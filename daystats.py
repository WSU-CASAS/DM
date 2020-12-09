#!/usr/bin/python

# daystats.py <data_file>+
#
# Extracts behavior markers from activity-labeled data
#
# Requires files: mobiledata

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import math
import os.path
import sys
from collections import Counter

import numpy as np

import config
import loc


class DayStats:

    def __init__(self):
        """ Constructor
        """
        self.lmappings = dict()
        self.lmappings['other'] = 'other'
        self.locations = list()
        self.samplerate = 1440

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
        Features are: total rotation, total acceleration,
        distance travelled, number of missing sensor readings,
        time spent on each oc activity (33),
        time spent on primary activity (12),
        first occurrence each oc activity (33),
        first occurrence primary activity (12),
        time spent at each location type (4),
        first occurrence at each location (4)
        """

        cf = config.Config()
        activity_names = cf.activity_list  # primary activities

        latitudes = data[:, cf.latitude]
        longitudes = data[:, cf.longitude]
        numfeatures = int(4 + (2 * cf.num_activities) +
                          (2 * len(activity_names)) + (2 * cf.num_locations))
        numdays = int(len(data) / self.samplerate)
        locarray = np.zeros(len(latitudes))
        for i in range(len(latitudes)):
            locarray[i] = generate_location(latitudes[i], longitudes[i], location)
        day_values = np.zeros((numdays, numfeatures))
        for i in range(numdays):
            day_rotation = 0.0
            day_acceleration = 0.0
            day_missing = 0.0
            day_distance = 0.0
            xvalue = 0.0
            yvalue = 0.0
            begin_day = i * self.samplerate
            for j in range(self.samplerate):
                num = begin_day + j
                element = data[num]
                rotation = (element[cf.x_rotation] * element[cf.x_rotation]) + \
                           (element[cf.y_rotation] * element[cf.y_rotation]) + \
                           (element[cf.z_rotation] * element[cf.z_rotation])
                day_rotation += rotation
                acceleration = (element[cf.x_acceleration] * element[cf.x_acceleration]) + \
                               (element[cf.y_acceleration] * element[cf.y_acceleration]) + \
                               (element[cf.z_acceleration] * element[cf.z_acceleration])
                day_acceleration += acceleration
                day_missing += element[cf.missing_value_pos]
                if j > 1:
                    xdist = element[cf.latitude] - xvalue
                    ydist = element[cf.longitude] - yvalue
                    day_distance += math.sqrt((xdist * xdist) + (ydist * ydist))
                xvalue = element[cf.latitude]
                yvalue = element[cf.longitude]
            day_values[i][0] = day_rotation
            day_values[i][1] = day_acceleration
            day_values[i][2] = day_distance
            day_values[i][3] = day_missing
            end_day = begin_day + self.samplerate  # one day for primary activity
            actsubset = data[begin_day:end_day, cf.activity_pos]
            astart = 4
            # time spent on each activity, index 4..36
            for j in range(cf.num_activities):
                counter = Counter(data[begin_day:end_day, cf.oneclass_pos + j])
                day_values[i][j + astart] = counter[1.0]

            # time spent on primary activity, index 37..48
            for j in range(len(activity_names)):
                day_values[i][j + astart + cf.num_activities] = np.sum(actsubset == float(j))

            # time of first occurrence for each activity, index 49..81
            for j in range(cf.num_activities):
                asubset = data[begin_day:end_day, cf.oneclass_pos + j]
                if j not in asubset:
                    occurrence_time = -1
                else:
                    occurrence_time = np.where(asubset == float(j))[0][0]
                    occurrence_time = occurrence_time // 60
                day_values[i][j + astart + cf.num_activities + len(activity_names)] = \
                    occurrence_time

            # time of first occurrence for activity label, index 82..93
            for j in range(len(activity_names)):
                if j not in actsubset:
                    occurrence_time = -1
                else:
                    occurrence_time = np.where(actsubset == float(j))[0][0] // 60
                day_values[i][j + astart + (2 * cf.num_activities) + len(activity_names)] = \
                    occurrence_time

            locsubset = locarray[begin_day:end_day]
            lstart = astart + (2 * cf.num_activities) + (2 * len(activity_names))

            # time spent at location, index 94..98
            for j in range(cf.num_locations):
                np.set_printoptions(threshold=sys.maxsize)
                day_values[i][j + lstart] = np.sum(locsubset == float(j))

            # time of first location visit, index 99..102
            for j in range(cf.num_locations):
                if j not in locsubset:
                    occurrence_time = -1
                else:
                    occurrence_time = np.where(locsubset == float(j))[0][0] // 60
                day_values[i][j + lstart + cf.num_locations] = occurrence_time
        return day_values

    def day_stats(self, data, location):
        """ Generate markers that describe one day of behavior data.
        """
        if location is None:
            location = loc.Location()
            location.read_location_mappings()
        locations_index = location.read_locations()
        return self.extract_features(data, location)


def generate_location(latitude, longitude, location):
    """ Generate the index corresponding to a location type for input
        latitude and longitude.
    """
    location_type = location.find_location(latitude, longitude)
    name = location.map_location_name(location_type)
    return location.generate_location_num(name)


def main(filename):
    day = DayStats()
    cf = config.Config()
    infile = os.path.join(cf.datapath, filename + '.minute')
    outfile = os.path.join(cf.datapath, filename + '.dayvalues')

    data = np.loadtxt(infile, dtype=float, delimiter=',')
    n = len(data)
    zeros = np.zeros((n, 1))
    data = np.hstack((data, zeros))
    day_values = day.day_stats(data, None)
    np.savetxt(outfile, day_values, delimiter=',')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need to specify filename\n")
        exit()
    main(sys.argv[1])
