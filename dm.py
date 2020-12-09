#!/usr/bin/python

# python dm.py <data_file>
#
# Extract digital behavior markers from activity-labeled sensor data.
#
# Input is a csv file containing sensor data.
# Output is a one-line csv file containing a set of behavior markers.

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import os.path
import sys

import numpy as np
import pandas as pd

import bcd
import bstats
import config
import daystats
import downsample
import hourstats
import impute
import loc
import printheader


class DM:

    def __init__(self, data_filename=None):
        """ Constructor
        """
        if data_filename is None:
            self.infile = "data"
        else:
            self.infile = data_filename
        self.cf = config.Config()

    def find_activity(self, label):
        """ Return the index of the input activity name in the activity list
        """
        n = len(self.cf.activity_list)
        for i in range(n):
            if self.cf.activity_list[i] == label:
                return float(i)
        return 0.0

    def init_data(self, filename):
        """ Read activity-labeled sensor data from a file.
        Return the string-based activity label with a corresponding number and
        return the data matrix.
        """
        infile = os.path.join(self.cf.datapath, filename)
        df = pd.read_csv(infile, header=None)
        n = df.shape[0]
        numfeatures = df.shape[1]
        data = np.zeros(df.shape, dtype=float)
        # replace activity label (last feature) with the corresponding index number
        for i in range(n):
            for j in range(numfeatures - 1):
                data[i][j] = float(df[j][i])
            position = self.find_activity(df[numfeatures - 1][i])
            data[i][numfeatures - 1] = float(position)
        return data


def main():
    dm = DM()
    filename = dm.cf.set_parameters(sys.argv)
    if filename is None:
        print("Supply a filename that contains the minute data.")
        exit()
    location = loc.Location()
    location.read_location_mappings()
    infile = os.path.join(dm.cf.datapath, filename)
    data = np.loadtxt(infile, delimiter=',')
    data = downsample.downsample(data)
    data = impute.impute_values(data)
    day = daystats.DayStats()  # Generate daily behavior features
    day_values = day.day_stats(data, location)
    hour = hourstats.HourStats()  # Generate hourly behavior features
    hour_values = hour.hour_stats(data, location)
    bm = bstats.BehaviorStats()  # Generate global behavior features
    behavior_markers = bm.behavior_stats(day_values, hour_values)
    behavior_change = bcd.BCD()  # Generate weekly change from baseline
    change_scores = behavior_change.bcd(day_values, hour_values)
    printheader.print_markers(filename, day_values, hour_values,
                              behavior_markers, change_scores, dm, day, hour, bm, False)


if __name__ == "__main__":
    main()
