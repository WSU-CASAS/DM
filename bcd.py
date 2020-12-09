#!/usr/bin/python

# bcd.py <data_file>+
#
# Compute behavioral change detection scores for each week of data.

# Written by Gina Sprint
# and modified by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import os.path
import sys

import numpy as np

import config


class BCD:

    def __init__(self):
        """ Constructor
        """
        self.num_permutations = 1000  # number of permutations to test

    @staticmethod
    def kl_divergence(p, q):
        """ Compute the Kullback-Leibler divergence between two input distributions.
        """
        p = np.asarray(p, dtype=np.float)
        q = np.asarray(q, dtype=np.float)
        kl_sum1 = 0
        kl_sum2 = 0
        for i in range(0, p.size):
            if p[i] != 0.0 and q[i] != 0.0:
                v1 = p[i] / q[i]
                v2 = q[i] / p[i]
                if v1 != 0.0:
                    kl_sum1 += float(p[i] * np.log(v1))
                if v2 != 0.0:
                    kl_sum2 += float(q[i] * np.log(v2))
        temp = (kl_sum1 + kl_sum2) / 2  # symmetric kl divergence
        return temp

    @staticmethod
    def normalize_change_score(p_vals, alpha_star=0.01):
        """ Normalize the change scores to lie in the range [0.0, 1.0].
        """
        m = len(p_vals)
        sig_changes_count = 0
        p_vals.sort()
        threshold = np.zeros(m)
        for i in range(1, m + 1):
            threshold = i * alpha_star / m
            if p_vals[i - 1] <= threshold:
                sig_changes_count += 1
        sig_changes_count /= float(len(p_vals))
        if sig_changes_count > 1.0:
            sig_changes_count = 1.0
        return sig_changes_count

    @staticmethod
    def test_permute_days_significance(pvector, distance, permute_days_cutoff):
        """ Determine the statistical significance of the results formed by
        permutation testing.
        """
        nump = len(pvector)
        greater_count = 0
        for i in range(nump):
            if pvector[i] >= distance:
                greater_count += 1
        return float(greater_count) / float(nump)

    def permutation_change(self, w1, w2):
        """ Small-window Permutation-based Change Detection in Activity Routine.
        """
        permute_days_cutoff = 0.05
        num_days = 7

        # collapse week into single average day
        baseline_df = np.apply_along_axis(np.sum, 0, w1)
        curr_df = np.apply_along_axis(np.sum, 0, w2)

        baseline_distance = np.zeros(24)
        # compute hourly day change based on symmetric Kullback-Leibler divergence
        for i in range(24):
            baseline_distance[i] = self.kl_divergence(baseline_df[i], curr_df[i])

        p_vals = list()
        data = np.concatenate((w1, w2), axis=0)
        # compute pairwise day change for shuffled days
        new_distance = np.zeros((self.num_permutations, 24))
        for i in range(self.num_permutations):
            shuffle_inds = np.random.permutation(2 * num_days)
            first_half = data[shuffle_inds[:num_days]]
            second_half = data[shuffle_inds[-num_days:]]
            first_df = np.apply_along_axis(np.sum, 0, first_half)
            second_df = np.apply_along_axis(np.sum, 0, second_half)
            # compute change based on symmetric Kullback-Leibler divergence
            for j in range(24):
                new_distance[i][j] = self.kl_divergence(p=first_df[j],
                                                        q=second_df[j])
        for i in range(self.num_permutations):
            for j in range(24):
                p_val = self.test_permute_days_significance(
                    pvector=new_distance[:, j],
                    distance=baseline_distance[j],
                    permute_days_cutoff=permute_days_cutoff)
                p_vals.append(p_val)

        cs = 1.0 - np.absolute(np.mean(p_vals))
        results = self.normalize_change_score(p_vals=p_vals,
                                              alpha_star=permute_days_cutoff)
        if results >= 0.95:
            is_sig = 1
        else:
            is_sig = 0
        return cs, is_sig

    @staticmethod
    def compute_box_outlier_significance(potential_outlier, sample):
        """ Determine whether current week is an outlier with respect to
        time-permuted version of the weeks.
        """
        is_sig = 0
        q1 = np.percentile(sample, 25)
        q3 = np.percentile(sample, 75)
        iqr = q3 - q1
        upper_fence = q3 + 1.5 * iqr
        if potential_outlier > upper_fence:
            is_sig = 1
        return upper_fence, is_sig

    @staticmethod
    def normalize_scores(cs, scores):
        """ Normalize the change scores to be in the range [0.0, 1.0].
        """
        temp = np.append(scores, cs)
        min_value = np.min(temp)
        max_value = np.max(temp)
        diff = max_value - min_value
        new_cs = (cs - min_value) / diff
        n = len(scores)
        new_scores = np.zeros(n)
        for i in range(n):
            new_scores[i] = (scores[i] - min_value) / diff
        return new_cs, new_scores

    def test_window_change_significance(self, cs, scores):
        """ Use boxplot analysis to determine if the current week's change from
        baseline is significant.
        """
        # cs, scores = self.normalize_scores(cs, scores)
        cutoffs = list()
        sigs = list()
        for i in cs:
            cutoff, is_sig = self.compute_box_outlier_significance(i, scores)
            if cutoff == 0.0:
                cutoffs.append(0.0)
            else:
                cutoffs.append(i / cutoff)
            sigs.append(is_sig)
        if np.mean(sigs) >= 0.5:
            is_sig = 1
        else:
            is_sig = 0
        return np.mean(cutoffs), is_sig

    @staticmethod
    def normalize_daydata(data):
        """ Normalize daily statistics to be in range [0,1].
        """
        n = len(data)
        k = len(data[0])
        for i in range(k):
            min_value = np.min(data[:, i])
            max_value = np.max(data[:, i])
            diff = max_value - min_value
            if diff > 0.0:
                for j in range(n):
                    data[j][i] = (data[j][i] - min_value) / diff
        return data

    @staticmethod
    def normalize_hourdata(flat_data, data):
        """ Normalize hourly statistics to be in range [0,1].
        """
        n = len(data)
        dim = len(data[0][0])
        for k in range(dim):
            min_value = np.min(flat_data[:, k])
            max_value = np.max(flat_data[:, k])
            diff = max_value - min_value
            if diff > 0.0:
                for i in range(n):
                    for j in range(24):
                        data[i][j][k] = (data[i][j][k] - min_value) / diff
        return data

    def compute_change_scores(self, days1, days2, hours1, hours2):
        """ Compute change scores using one or more measures.
        Currently employs small-window Permutation Change.
        """
        cs1, is_sig1 = self.permutation_change(hours1, hours2)
        return cs1, is_sig1

    def check_trend(self, daydata, flat_hourdata, hourdata):
        """ Compute change between first week (baseline) and all following weeks.
        """
        results = list()
        daydata = self.normalize_daydata(daydata)
        hourdata = self.normalize_hourdata(flat_hourdata, hourdata)
        numdays = len(daydata)
        numweeks = int(numdays / 7)
        baseline_week_daydata = daydata[:7, :]

        # trim first day because it may be incomplete
        baseline_week_hourdata = hourdata[:7, :]
        for i in range(numweeks):
            start = i * 7
            stop = i * 7 + 7
            compare_week_daydata = daydata[start:stop, :]
            k = len(hourdata[0][0])
            compare_week_hourdata = hourdata[start:stop, :]
            cs, is_sig = self.compute_change_scores(baseline_week_daydata,
                                                    compare_week_daydata,
                                                    baseline_week_hourdata,
                                                    compare_week_hourdata)
            results.append((cs, is_sig))
        return results

    def bcd(self, daydata, hourdata):
        """ Perform behavioral change detection.
        """
        numdays = int(len(hourdata) / 24)
        numfeatures = len(hourdata[0])
        reshaped_hourdata = np.reshape(hourdata, (numdays, 24, numfeatures))
        if len(daydata) < 8:
            return [(0, 0)]
        else:
            return self.check_trend(daydata, hourdata, reshaped_hourdata)


def main(bcd_obj, main_days_infile, main_hours_infile):
    """ Load day and hour statistics from files. Use these values to perform
    behavioral change detection.
    """
    daydata = np.loadtxt(main_days_infile, dtype=float, delimiter=',')
    hourdata = np.loadtxt(main_hours_infile, dtype=float, delimiter=',')
    print(bcd_obj.bcd(daydata, hourdata))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Need to specify a user ID\n")
        sys.exit()

    bcd = BCD()
    cf = config.Config()
    days_infile = os.path.join(cf.datapath, sys.argv[1] + '.dayvalues')
    hours_infile = os.path.join(cf.datapath, sys.argv[1] + '.hourvalues')
    main(bcd, days_infile, hours_infile)
