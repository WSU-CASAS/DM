#!/usr/bin/python

# impute.py <data_file>+
#
# Impute missing values

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import os.path
import sys
from collections import Counter

import numpy as np

import config


def most_frequent(values):
    """ Identify the value that occurs most frequently in the input array.
    """
    if len(values) == 0:
        return 0
    else:
        counts = Counter(values)
        return counts.most_common(1)[0][0]


def generate_medians(cf, data):
    """ Create an array containing the median values of the sensor values.
    """
    yaw = np.median(data[:, cf.yaw])
    pitch = np.median(data[:, cf.pitch])
    roll = np.median(data[:, cf.roll])
    rotx = np.median(data[:, cf.x_rotation])
    roty = np.median(data[:, cf.y_rotation])
    rotz = np.median(data[:, cf.z_rotation])
    accx = np.median(data[:, cf.x_acceleration])
    accy = np.median(data[:, cf.y_acceleration])
    accz = np.median(data[:, cf.z_acceleration])
    latitude = most_frequent(data[:, cf.latitude])
    longitude = most_frequent(data[:, cf.longitude])
    altitude = most_frequent(data[:, cf.altitude])
    course = np.median(data[:, cf.course])
    speed = np.median(data[:, cf.speed])
    hacc = np.median(data[:, cf.horizontal_accuracy])
    vacc = np.median(data[:, cf.vertical_accuracy])
    activity_medians = np.zeros(cf.num_activities)
    for i in range(cf.num_activities):  # one class activity labels
        activity_medians[i] = most_frequent(data[:, i + cf.num_sensors])
    activity = most_frequent(data[:, cf.activity_pos])  # activity
    medians = [yaw, pitch, roll, rotx, roty, rotz, accx, accy, accz,
               latitude, longitude, altitude, course, speed, hacc, vacc]
    medians = np.append(medians, activity_medians)
    medians = np.append(medians, activity)
    return medians


def replace(cf, i, rp_time, medians):
    """ Calculate value to impute.
    """
    if i == cf.date:
        return int(rp_time / cf.minutes_in_day)
    elif i == cf.time:
        return rp_time % cf.minutes_in_day
    else:
        return medians[i - 2]


def impute_values(data):
    """ Generate sensor entries for time values between the begin and end
    of the input data that have no entries.
    This function considers three cases:
    1. No entries between midnight and the first reported time on the first day
       of data collection, the function generates those.
    2. No entries between the last reported time on the last day of
       data collection and the end of that day, the function generates those.
    3. A missing chunk of data between the first and last reported times.
    """
    cf = config.Config()
    # new size is |sensors| + |activities| + activity label + missingvalue
    numsensors = cf.num_sensors + cf.num_activities + 2
    medians = generate_medians(cf, data)
    begin_date = int(data[0][0])
    end_date = int(data[len(data) - 1][0])
    new_size = int((end_date - begin_date) + 1) * cf.minutes_in_day  # total minutes
    new_data = np.zeros((new_size, numsensors))
    n = len(data)
    prevtime = (begin_date * cf.minutes_in_day)  # start at midnight on first day
    date = data[0][cf.date]
    impute_time = data[0][cf.time]
    current_time = int(date * cf.minutes_in_day) + impute_time  # time in minutes
    count = missing = element = 0
    while element < n:
        if prevtime < current_time:  # impute missing values at beginning
            for i in range(numsensors - 1):
                new_data[count][i] = replace(cf, i, prevtime, medians)
            new_data[count][cf.missing_value_pos] = 1
            missing += 1
        else:  # copy actual value
            for i in range(numsensors - 1):
                new_data[count][i] = data[element][i]
            element += 1
            if element < n:
                date = data[element][cf.date]
                impute_time = data[element][cf.time]
                current_time = int(date * cf.minutes_in_day) + int(impute_time / 60)
        count += 1
        prevtime += 1
    while count < new_size:  # fill in missing values on last data day
        for i in range(numsensors - 1):
            new_data[count][i] = replace(cf, i, prevtime, medians)
        new_data[count][cf.missing_value_pos] = 1
        count += 1
        missing += 1
    return new_data


def main(filename):
    cf = config.Config()
    infile = os.path.join(cf.datapath, filename + '.combine')
    outfile = os.path.join(cf.datapath, filename + '.completed')

    data = np.loadtxt(infile, dtype=float, delimiter=',')
    new_data = impute_values(data)
    np.savetxt(outfile, new_data, delimiter=',')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need to specify filename\n")
        exit()
    main(sys.argv[1])
