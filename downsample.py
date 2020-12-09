#!/usr/bin/python

# downsample.py <data_file>+
#
# Downsamples feature vector from multiple readings per second to
# one reading per minute.

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import os.path
import sys

import numpy as np

import config

# global variables
original_sample_rate = 1  # number of samples per second
new_sample_rate = 1
downrate = int(original_sample_rate / new_sample_rate)


def seconds_to_minutes(seconds):
    """ Map time of day in seconds past midnight to time of day in
    minutes past midnight.
    """
    return int(seconds / 60)


def downsample(data):
    """ Downsample sensor data. This function assumes that the original
    sample rate is higher than the new sample rate. To downsample, values
    are aggregated over a window of sensor values.
    Numeric sensor values are replaced by the mean over the window.
    For date, location, and activity, the most recent value is used.
    """
    cf = config.Config()
    n = len(data)
    k = len(data[0])
    window_size = int(n / downrate)
    newdata = np.empty((window_size, k))

    for i in range(window_size):  # aggregate values over window
        newdata[i][cf.date] = data[i * downrate][cf.date]  # last value
        newdata[i][cf.time] = seconds_to_minutes(data[i * downrate][cf.time])
        newdata[i][cf.latitude] = data[i * downrate][cf.latitude]
        newdata[i][cf.longitude] = data[i * downrate][cf.longitude]
        newdata[i][cf.altitude] = data[i * downrate][cf.altitude]
        for j in (cf.yaw, cf.pitch, cf.roll,  # mean
                  cf.x_rotation, cf.y_rotation, cf.z_rotation,
                  cf.x_acceleration, cf.y_acceleration,
                  cf.z_acceleration, cf.latitude, cf.longitude,
                  cf.altitude, cf.course, cf.speed,
                  cf.horizontal_accuracy, cf.vertical_accuracy):
            newdata[i][j] = np.mean(data[i * downrate:(i * downrate) + downrate, j])
        for j in range(18, k):  # use last one-class and primary activity labels
            newdata[i][j] = data[i * downrate][j]
    return newdata


def main(filename):
    cf = config.Config()
    # Already complete.
    infile = os.path.join(cf.datapath, filename + '.combine')
    outfile = os.path.join(cf.datapath, filename + '.minute')
    data = np.loadtxt(infile, dtype=float, delimiter=',')
    minute_values = downsample(data)
    np.savetxt(outfile, minute_values, delimiter=',')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need to specify filename\n")
        exit()
    main(sys.argv[1])
