#!/usr/bin/python

# Contains utility functions.

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


from datetime import datetime


def get_datetime(date, dt_time):
    """ Input is two strings representing a date and a time with the format
    YYYY-MM-DD HH:MM:SS.ms. This function converts the two strings to a single
    datetime.datetime() object.
    """
    dt_str = date + ' ' + dt_time
    if '.' in dt_str:  # Remove optional millsecond precision
        dt_str = dt_str.split('.', 1)[0]
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    return dt


def clean(value, low, high):
    """ Clean up values that fall outside of a specified range.
    Replace outliers with the range min or max.
    """
    if value > high:
        return high
    elif value < low:
        return low
    else:
        return value
