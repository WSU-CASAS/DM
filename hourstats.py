#!/usr/bin/python

# hourstats.py <data_file>+
#
# Extracts behavior markers from mobile data.
#
# Requires files: mobiledata

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2019. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import os.path
import sys
from collections import Counter

import numpy as np

import config
import daystats
import loc


class HourStats:

    def __init__(self):
        """ Constructor
        """
        self.lmappings = dict()
        self.lmappings['other'] = 'other'
        self.locations = list()
        self.samplerate = 60  # number of samples per hour
        self.cf = config.Config()

    def read_location_mappings(self):
        """ Generate a translate list for location names.
        This function assumes that file l.translate exists in the same directory
        as the code. File l.translate contains an arbitrary number of lines, each
        with syntax "specificType mappedType". This function maps locations of
        specificType to the corresponding, more general, mappedType.
        """
        with open('l.translate', "r") as file:
            for line in file:
                x = str(str(line).strip()).split(' ', 2)
                self.lmappings[x[0]] = x[1]

    def extract_features(self, data, location):
        """ Extract feature vector.
        Features are:
        total rotation, total acceleration, distance travelled,
        number of missing values,
        time spent on each oc activity (33),
        time spent on primary activity (12),
        time spent at each location type (4)
        """

        latitudes = data[:, self.cf.latitude]
        longitudes = data[:, self.cf.longitude]
        locarray = np.zeros(len(latitudes))
        for i in range(len(latitudes)):
            locarray[i] = daystats.generate_location(latitudes[i], longitudes[i], location)
        numfeatures = int(4 + self.cf.num_activities + len(self.cf.activity_list) +
                          self.cf.num_locations)
        numhours = int(len(data) / self.samplerate)
        hour_values = np.zeros((numhours, numfeatures))
        for i in range(numhours):
            hour_rotation = 0.0
            hour_acceleration = 0.0
            hour_missing = 0.0
            hour_distance = 0.0
            begin_hour = i * 60
            xvalue = 0.0
            yvalue = 0.0
            for j in range(self.samplerate):
                num = begin_hour + j
                element = data[num]
                rotation = (element[self.cf.x_rotation] * element[self.cf.x_rotation]) + \
                           (element[self.cf.y_rotation] * element[self.cf.y_rotation]) + \
                           (element[self.cf.z_rotation] * element[self.cf.z_rotation])
                hour_rotation += rotation
                acceleration = (element[self.cf.x_acceleration] *
                                element[self.cf.x_acceleration]) + \
                               (element[self.cf.y_acceleration] *
                                element[self.cf.y_acceleration]) + \
                               (element[self.cf.z_acceleration] *
                                element[self.cf.z_acceleration])
                hour_acceleration += acceleration
                hour_missing += element[self.cf.missing_value_pos]
                if j > 1:
                    xdist = element[self.cf.latitude] - xvalue
                    ydist = element[self.cf.longitude] - yvalue
                    hour_distance += (xdist * xdist) + (ydist * ydist)
                xvalue = element[self.cf.latitude]
                yvalue = element[self.cf.longitude]
            hour_values[i][0] = hour_rotation
            hour_values[i][1] = hour_acceleration
            hour_values[i][2] = hour_distance
            hour_values[i][3] = hour_missing

            end_hour = begin_hour + self.samplerate
            actsubset = data[begin_hour:end_hour, self.cf.activity_pos]
            astart = 4

            # time spent on each activity, index 4..36
            for j in range(self.cf.num_activities):
                counter = Counter(data[begin_hour:end_hour, self.cf.oneclass_pos + j])
                hour_values[i][j + astart] = counter[1.0]

            # time spent on primary activity, index 37..48
            for j in range(len(self.cf.activity_list)):
                hour_values[i][j + astart + self.cf.num_activities] = np.sum(actsubset == float(j))

            # time spent at location, index 49..52
            locsubset = locarray[begin_hour:end_hour]
            lstart = astart + self.cf.num_activities + len(self.cf.activity_list)
            for j in range(self.cf.num_locations):  # time spent at each location
                hour_values[i][j + lstart] = np.sum(locsubset == float(j))
        return hour_values

    def hour_stats(self, data, location):
        """ Generate markers that describe one hour of behavior data.
        """
        if location is None:
            location = loc.Location()
            location.read_location_mappings()
        locations_index = location.read_locations()
        return self.extract_features(data, location)


def main(filename):
    hour = HourStats()
    cf = config.Config()
    infile = os.path.join(cf.datapath, filename + '.minute')
    outfile = os.path.join(cf.datapath, filename + '.hourvalues')

    data = np.loadtxt(infile, dtype=float, delimiter=',')
    n = len(data)
    zeros = np.zeros((n, 1))
    data = np.hstack((data, zeros))
    hour_values = hour.hour_stats(data, None)
    np.savetxt(outfile, hour_values, delimiter=',')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need to specify filename\n")
        exit()
    main(sys.argv[1])
