#!/usr/bin/python

# b.py <data_file>+
#
# Extracts behavior markers from mobile data.

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import os.path
import sys

import numpy as np

import config
import features


class BehaviorStats:

    def __init__(self):
        """ Constructor
        """

    @staticmethod
    def twod_features(data, means, medians, stds):
        """ Generate markers from 2D features.
        """
        zc = np.empty_like(means)
        mc = np.empty_like(means)
        iqr = np.empty_like(means)
        skew = np.empty_like(means)
        k = np.empty_like(means)
        for i in range(len(data[0])):
            zc = features.zero_crossings(data[:, i], medians[i])
            mc = features.mean_crossings(data[:, i], means[i])
            iqr = features.interquartile_range(data[:, i])
            skew = features.skewness(data[:, i], means[i])
            k = features.kurtosis(data[:, i], means[i], stds[i])
        return zc, mc, iqr, skew, k

    @staticmethod
    def normalize(data):
        """ Normalize input data to fall in range [-0.5, 0.5].
        """
        minvalue = np.min(data)
        maxvalue = np.max(data)
        valrange = maxvalue - minvalue
        vals = np.zeros(len(data))
        for i in range(len(data)):
            if valrange == 0.0:
                vals[i] = -0.5
            else:
                vals[i] = ((data[i] - minvalue) / valrange) - 0.5
        return vals

    @staticmethod
    def compute_new_days(new_days, days):
        """ Aggregate multiple weeks by computing the means of a feature
        for each day of the week.
        (date mod 7) == 0 F, 1 Sa, 2 Su, 3 M, 4 Tu, 5 W, 6 Th
        """
        if len(days[3::7]) > 0:  # Friday
            new_days[0] = np.apply_along_axis(np.mean, 0, days[3::7])
        else:
            new_days[0] = 0.0
        if len(days[4::7]) > 0:  # Saturday
            new_days[1] = np.apply_along_axis(np.mean, 0, days[4::7])
        else:
            new_days[1] = 0.0
        if len(days[5::7]) > 0:  # Sunday
            new_days[2] = np.apply_along_axis(np.mean, 0, days[5::7])
        else:
            new_days[2] = 0.0
        if len(days[6::7]) > 0:  # Monday
            new_days[3] = np.apply_along_axis(np.mean, 0, days[6::7])
        else:
            new_days[3] = 0.0
        if len(days[0::7]) > 0:  # Tuesday
            new_days[4] = np.apply_along_axis(np.mean, 0, days[0::7])
        else:
            new_days[4] = 0.0
        if len(days[1::7]) > 0:  # Wednesday
            new_days[5] = np.apply_along_axis(np.mean, 0, days[1::7])
        else:
            new_days[5] = 0.0
        if len(days[2::7]) > 0:  # Thursday
            new_days[6] = np.apply_along_axis(np.mean, 0, days[2::7])
        else:
            new_days[6] = 0.0  # default
        return new_days

    @staticmethod
    def ri_formula(ri_x, ri_y):
        """ Apply regularity index formula to a pair of features.
        """
        ri = 0.0
        for x, y in zip(ri_x, ri_y):
            ri += x * y
        ri /= 24.0
        return ri

    def regularity(self, feature):
        """ Compute regularity index for a single feature.
        The regularity between day a and b is defined as
        Sum_{t-1}^T feature(day a, time t) * feature(day b, time t) / T,
        where T = 24 hours.
        The data are first normalized to lie in the range [-0.5,0.5].
        """
        data = self.normalize(feature)
        numdays = int(len(feature) // 24)
        hours_in_a_week = 168
        numweeks = int(numdays // 7)
        vals = list()

        # break data into individual days
        days = [data[i * 24:(i + 1) * 24] for i in range((len(data) + 23) // 24)]
        new_days = [[0.0 for j in range(24)] for i in range(7)]
        new_days = self.compute_new_days(new_days, days)

        indices = list()  # pairs within week
        for i in range(7):
            for j in range(7):
                if i != j:
                    try:
                        if len(new_days[i]) != 0 and len(new_days[j]) != 0:
                            indices.append(self.ri_formula(new_days[i], new_days[j]))
                        else:
                            indices.append(0.0)
                    except:
                        indices.append(0.0)
        vals.append(np.mean(indices))

        indices = list()  # pairs within weekdays
        for i in range(5):
            for j in range(5):
                if i != j:
                    try:
                        if len(new_days[i]) != 0 and len(new_days[j]) != 0:
                            indices.append(self.ri_formula(new_days[i], new_days[j]))
                        else:
                            indices.append(0.0)
                    except:
                        indices.append(0.0)
        vals.append(np.mean(indices))

        indices = list()  # pairs between weeks
        if numweeks < 2:
            vals.append(0.0)
        else:
            for i in range(7):
                group_days = days[i::7]
                for j in range(numweeks):
                    for k in range(numweeks):
                        if j != k:
                            try:
                                if len(group_days[j]) != 0 and len(group_days[k]) != 0:
                                    indices.append(self.ri_formula(group_days[j], group_days[k]))
                                else:
                                    indices.append(0.0)
                            except:
                                indices.append(0.0)
                vals.append(np.mean(indices))
        return vals

    def regularity_index(self, hourdata):
        """ Compute regularity index for continuous-valued features based on
        formula found in Wang et al., IMWUT, 2018.
        Do not compute for date, time, or activity.
        """
        ri = []
        for i in range(3):
            vals = np.apply_along_axis(self.regularity, 0, hourdata[:, i])
            ri = np.append(ri, vals)
        return ri

    @staticmethod
    def circadian_rhythm(data):
        """ Compute circadian rhythm of a single feature.
        Compute a periodogram from the data, normalize the values,
        and extract the corresponding value for 24 (a 24 hour cycle).
        """
        fvals = np.fft.fft(data)  # compute a periodogram
        avals = np.absolute(fvals)
        avals = avals[1:]
        total = np.sum(avals)  # normalize the values
        if total != 0:
            avals = avals / total
        return avals[23]  # frequency value for a 24 hour cycle

    def circadian_rhythm_features(self, hourdata):
        """ Compute circadian rhythm of individual features based on hour data.
        Do not compute for activity, location, or missing indicator.
        """
        cr = list()
        for i in range(3):
            vals = np.apply_along_axis(self.circadian_rhythm, 0, hourdata[:, i])
            cr = np.append(cr, vals)
        return cr

    def extract_component_features(self, data):
        """ Compute statistics for each individual feature.
        """
        new_data = list()
        means = np.apply_along_axis(np.mean, 0, data)
        new_data = np.append(new_data, means)
        medians = np.apply_along_axis(np.median, 0, data)
        new_data = np.append(new_data, medians)
        stds = np.apply_along_axis(np.std, 0, data)
        new_data = np.append(new_data, stds)
        maxes = np.apply_along_axis(np.max, 0, data)
        new_data = np.append(new_data, maxes)
        mins = np.apply_along_axis(np.min, 0, data)
        new_data = np.append(new_data, mins)
        if len(data) == 1:  # only one time unit of data
            k = len(data[0])
            for i in range(k + 5):
                new_data = np.append(new_data, 0.0)  # zc, mc, iqr, skew, k, se
        else:
            zc, mc, iqr, skew, k = self.twod_features(data, means, medians, stds)
            new_data = np.append(new_data, zc)
            new_data = np.append(new_data, mc)
            new_data = np.append(new_data, iqr)
            new_data = np.append(new_data, skew)
            new_data = np.append(new_data, k)
            se = np.apply_along_axis(features.signal_energy, 0, data)
            new_data = np.append(new_data, se)
        return new_data

    def behavior_stats(self, daydata, hourdata):
        """ Extract digital behavior markers.
        Markers extracted from day and hour features:
        mean, median, standard deviation, zero crossings, mean crossings,
        interquartile range, skewness, kurtosis, signal energy
        regularity within week / between weeks / overall, circadian rhythm
        """
        new_data = []
        new_data = np.append(new_data, self.extract_component_features(daydata))
        new_data = np.append(new_data, self.extract_component_features(hourdata))
        if len(daydata) == 1:
            for i in range(12):
                new_data = np.append(new_data, 0.0)
        else:
            ri = self.regularity_index(hourdata)
            new_data = np.append(new_data, ri)
            cr = self.circadian_rhythm_features(hourdata)
            new_data = np.append(new_data, cr)
        return new_data


def main(filename):
    bstats = BehaviorStats()
    cf = config.Config()
    infile = os.path.join(cf.datapath, filename + '.dayvalues')
    hourfile = os.path.join(cf.datapath, filename + '.hourvalues')

    daydata = np.loadtxt(infile, dtype=float, delimiter=',')
    hourdata = np.loadtxt(hourfile, dtype=float, delimiter=',')
    main_features = bstats.behavior_stats(daydata, hourdata)
    outstr = ""
    for i in range(len(main_features)):
        outstr += str(main_features[i])
        if i < (len(main_features) - 1):
            outstr += ','
        else:
            outstr += '\n'
    out_filename = os.path.join(cf.datapath, filename + '.features')
    outfile = open(out_filename, "w")
    outfile.write(outstr)
    outfile.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need to specify filename\n")
        exit()
    main(sys.argv[1])
