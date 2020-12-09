#!/usr/bin/python

# printheader.py <data_file>+
#
# Create headers for markers.
#

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import numpy as np
import os.path

import config


def generate_day_header():
    """ Print header line with feature names for day statistics.
    """
    outstr = "total_rotation,total_acceleration,total_distance,number_missing,"
    outstr += "oc1_time,oc2_time,oc3_time,oc4_time,oc5_time,oc6_time,oc7_time,"
    outstr += "oc8_time,oc9_time,oc10_time,oc11_time,oc12_time,oc13_time,"
    outstr += "oc14_time,oc15_time,oc16_time,oc17_time,oc18_time,oc19_time,"
    outstr += "oc20_time,oc21_time,oc22_time,oc23_time,oc24_time,oc25_time,"
    outstr += "oc26_time,oc27_time,oc28_time,oc29_time,oc30_time,oc31_time,"
    outstr += "oc32_time,oc33_time,activity1_time,activity2_time,"
    outstr += "activity3_time,activity4_time,activity5_time,activity6_time,"
    outstr += "activity7_time,activity8_time,activity9_time,activity10_time,"
    outstr += "activity11_time,activity12_time,oc1_first,oc2_first,"
    outstr += "oc3_first,oc4_first,oc5_first,oc6_first,oc7_first,oc8_first,"
    outstr += "oc9_first,oc10_first,oc11_first,oc12_first,oc13_first,"
    outstr += "oc14_first,oc15_first,oc16_first,oc17_first,oc18_first,"
    outstr += "oc19_first,oc20_first,oc21_first,oc22_first,oc23_first,"
    outstr += "oc24_first,oc25_first,oc26_first,oc27_first,oc28_first,"
    outstr += "oc29_first,oc30_first,oc31_first,oc32_first,oc33_first,"
    outstr += "activity1_first,activity2_first,activity3_first,activity4_first,"
    outstr += "activity5_first,activity6_first,activity7_first,activity8_first,"
    outstr += "activity9_first,activity10_first,activity11_first,"
    outstr += "activity12_first,location1_time,location2_time,location3_time,"
    outstr += "location4_time,location1_first,location2_first,location3_first,"
    outstr += "location4_first"
    return outstr


def generate_hour_header():
    """ Print header line with feature names for hour statistics.
    """
    outstr = "total_rotation,total_acceleration,total_distance,number_missing,"
    outstr += "oc1_time,oc2_time,oc3_time,oc4_time,oc5_time,oc6_time,oc7_time,"
    outstr += "oc8_time,oc9_time,oc10_time,oc11_time,oc12_time,oc13_time,"
    outstr += "oc14_time,oc15_time,oc16_time,oc17_time,oc18_time,oc19_time,"
    outstr += "oc20_time,oc21_time,oc22_time,oc23_time,oc24_time,oc25_time,"
    outstr += "oc26_time,oc27_time,oc28_time,oc29_time,oc30_time,oc31_time,"
    outstr += "oc32_time,oc33_time,activity1_time,activity2_time,"
    outstr += "activity3_time,activity4_time,activity5_time,activity6_time,"
    outstr += "activity7_time,activity8_time,activity9_time,activity10_time,"
    outstr += "activity11_time,activity12_time,"
    outstr += "location1_time,location2_time,location3_time,location4_time"
    return outstr


def generate_behavior_header():
    """ Print header line with feature names for overall behavior statistics.
    """
    outstr = "mean_day_f1,mean_day_f2,mean_day_f3,mean_day_f4,mean_day_f5,"
    outstr += "mean_day_f6,mean_day_f7,mean_day_f8,mean_day_f9,mean_day_f10,"
    outstr += "mean_day_f11,mean_day_f12,mean_day_f13,mean_day_f14,mean_day_f15,"
    outstr += "mean_day_f16,mean_day_f17,mean_day_f18,mean_day_f19,mean_day_f20,"
    outstr += "mean_day_f21,mean_day_f22,mean_day_f23,mean_day_f24,mean_day_f25,"
    outstr += "mean_day_f26,mean_day_f27,mean_day_f28,mean_day_f29,mean_day_f30,"
    outstr += "mean_day_f31,mean_day_f32,mean_day_f33,mean_day_f34,mean_day_f35,"
    outstr += "mean_day_f36,mean_day_f37,mean_day_f38,mean_day_f39,mean_day_f40,"
    outstr += "mean_day_f41,mean_day_f42,mean_day_f43,mean_day_f44,mean_day_f45,"
    outstr += "mean_day_f46,mean_day_f47,mean_day_f48,mean_day_f49,mean_day_f50,"
    outstr += "mean_day_f51,mean_day_f52,mean_day_f53,mean_day_f54,mean_day_f55,"
    outstr += "mean_day_f56,mean_day_f57,mean_day_f58,mean_day_f59,mean_day_f60,"
    outstr += "mean_day_f61,mean_day_f62,mean_day_f63,mean_day_f64,mean_day_f65,"
    outstr += "mean_day_f66,mean_day_f67,mean_day_f68,mean_day_f69,mean_day_f70,"
    outstr += "mean_day_f71,mean_day_f72,mean_day_f73,mean_day_f74,mean_day_f75,"
    outstr += "mean_day_f76,mean_day_f77,mean_day_f78,mean_day_f79,mean_day_f80,"
    outstr += "mean_day_f81,mean_day_f82,mean_day_f83,mean_day_f84,mean_day_f85,"
    outstr += "mean_day_f86,mean_day_f87,mean_day_f88,mean_day_f89,mean_day_f90,"
    outstr += "mean_day_f91,mean_day_f92,mean_day_f93,mean_day_f94,mean_day_f95,"
    outstr += "mean_day_f96,mean_day_f97,mean_day_f98,mean_day_f99,"
    outstr += "mean_day_f100,mean_day_f101,mean_day_f102,"
    outstr += "med_day_f1,med_day_f2,med_day_f3,med_day_f4,med_day_f5,"
    outstr += "med_day_f6,med_day_f7,med_day_f8,med_day_f9,med_day_f10,"
    outstr += "med_day_f11,med_day_f12,med_day_f13,med_day_f14,med_day_f15,"
    outstr += "med_day_f16,med_day_f17,med_day_f18,med_day_f19,med_day_f20,"
    outstr += "med_day_f21,med_day_f22,med_day_f23,med_day_f24,med_day_f25,"
    outstr += "med_day_f26,med_day_f27,med_day_f28,med_day_f29,med_day_f30,"
    outstr += "med_day_f31,med_day_f32,med_day_f33,med_day_f34,med_day_f35,"
    outstr += "med_day_f36,med_day_f37,med_day_f38,med_day_f39,med_day_f40,"
    outstr += "med_day_f41,med_day_f42,med_day_f43,med_day_f44,med_day_f45,"
    outstr += "med_day_f46,med_day_f47,med_day_f48,med_day_f49,med_day_f50,"
    outstr += "med_day_f51,med_day_f52,med_day_f53,med_day_f54,med_day_f55,"
    outstr += "med_day_f56,med_day_f57,med_day_f58,med_day_f59,med_day_f60,"
    outstr += "med_day_f61,med_day_f62,med_day_f63,med_day_f64,med_day_f65,"
    outstr += "med_day_f66,med_day_f67,med_day_f68,med_day_f69,med_day_f70,"
    outstr += "med_day_f71,med_day_f72,med_day_f73,med_day_f74,med_day_f75,"
    outstr += "med_day_f76,med_day_f77,med_day_f78,med_day_f79,med_day_f80,"
    outstr += "med_day_f81,med_day_f82,med_day_f83,med_day_f84,med_day_f85,"
    outstr += "med_day_f86,med_day_f87,med_day_f88,med_day_f89,med_day_f90,"
    outstr += "med_day_f91,med_day_f92,med_day_f93,med_day_f94,med_day_f95,"
    outstr += "med_day_f96,med_day_f97,med_day_f98,med_day_f99,"
    outstr += "med_day_f100,med_day_f101,med_day_f102,"
    outstr += "std_day_f1,std_day_f2,std_day_f3,std_day_f4,std_day_f5,"
    outstr += "std_day_f6,std_day_f7,std_day_f8,std_day_f9,std_day_f10,"
    outstr += "std_day_f11,std_day_f12,std_day_f13,std_day_f14,std_day_f15,"
    outstr += "std_day_f16,std_day_f17,std_day_f18,std_day_f19,std_day_f20,"
    outstr += "std_day_f21,std_day_f22,std_day_f23,std_day_f24,std_day_f25,"
    outstr += "std_day_f26,std_day_f27,std_day_f28,std_day_f29,std_day_f30,"
    outstr += "std_day_f31,std_day_f32,std_day_f33,std_day_f34,std_day_f35,"
    outstr += "std_day_f36,std_day_f37,std_day_f38,std_day_f39,std_day_f40,"
    outstr += "std_day_f41,std_day_f42,std_day_f43,std_day_f44,std_day_f45,"
    outstr += "std_day_f46,std_day_f47,std_day_f48,std_day_f49,std_day_f50,"
    outstr += "std_day_f51,std_day_f52,std_day_f53,std_day_f54,std_day_f55,"
    outstr += "std_day_f56,std_day_f57,std_day_f58,std_day_f59,std_day_f60,"
    outstr += "std_day_f61,std_day_f62,std_day_f63,std_day_f64,std_day_f65,"
    outstr += "std_day_f66,std_day_f67,std_day_f68,std_day_f69,std_day_f70,"
    outstr += "std_day_f71,std_day_f72,std_day_f73,std_day_f74,std_day_f75,"
    outstr += "std_day_f76,std_day_f77,std_day_f78,std_day_f79,std_day_f80,"
    outstr += "std_day_f81,std_day_f82,std_day_f83,std_day_f84,std_day_f85,"
    outstr += "std_day_f86,std_day_f87,std_day_f88,std_day_f89,std_day_f90,"
    outstr += "std_day_f91,std_day_f92,std_day_f93,std_day_f94,std_day_f95,"
    outstr += "std_day_f96,std_day_f97,std_day_f98,std_day_f99,"
    outstr += "std_day_f100,std_day_f101,std_day_f102,"
    outstr += "max_day_f1,max_day_f2,max_day_f3,max_day_f4,max_day_f5,"
    outstr += "max_day_f6,max_day_f7,max_day_f8,max_day_f9,max_day_f10,"
    outstr += "max_day_f11,max_day_f12,max_day_f13,max_day_f14,max_day_f15,"
    outstr += "max_day_f16,max_day_f17,max_day_f18,max_day_f19,max_day_f20,"
    outstr += "max_day_f21,max_day_f22,max_day_f23,max_day_f24,max_day_f25,"
    outstr += "max_day_f26,max_day_f27,max_day_f28,max_day_f29,max_day_f30,"
    outstr += "max_day_f31,max_day_f32,max_day_f33,max_day_f34,max_day_f35,"
    outstr += "max_day_f36,max_day_f37,max_day_f38,max_day_f39,max_day_f40,"
    outstr += "max_day_f41,max_day_f42,max_day_f43,max_day_f44,max_day_f45,"
    outstr += "max_day_f46,max_day_f47,max_day_f48,max_day_f49,max_day_f50,"
    outstr += "max_day_f51,max_day_f52,max_day_f53,max_day_f54,max_day_f55,"
    outstr += "max_day_f56,max_day_f57,max_day_f58,max_day_f59,max_day_f60,"
    outstr += "max_day_f61,max_day_f62,max_day_f63,max_day_f64,max_day_f65,"
    outstr += "max_day_f66,max_day_f67,max_day_f68,max_day_f69,max_day_f70,"
    outstr += "max_day_f71,max_day_f72,max_day_f73,max_day_f74,max_day_f75,"
    outstr += "max_day_f76,max_day_f77,max_day_f78,max_day_f79,max_day_f80,"
    outstr += "max_day_f81,max_day_f82,max_day_f83,max_day_f84,max_day_f85,"
    outstr += "max_day_f86,max_day_f87,max_day_f88,max_day_f89,max_day_f90,"
    outstr += "max_day_f91,max_day_f92,max_day_f93,max_day_f94,max_day_f95,"
    outstr += "max_day_f96,max_day_f97,max_day_f98,max_day_f99,"
    outstr += "max_day_f100,max_day_f101,max_day_f102,"
    outstr += "min_day_f1,min_day_f2,min_day_f3,min_day_f4,min_day_f5,"
    outstr += "min_day_f6,min_day_f7,min_day_f8,min_day_f9,min_day_f10,"
    outstr += "min_day_f11,min_day_f12,min_day_f13,min_day_f14,min_day_f15,"
    outstr += "min_day_f16,min_day_f17,min_day_f18,min_day_f19,min_day_f20,"
    outstr += "min_day_f21,min_day_f22,min_day_f23,min_day_f24,min_day_f25,"
    outstr += "min_day_f26,min_day_f27,min_day_f28,min_day_f29,min_day_f30,"
    outstr += "min_day_f31,min_day_f32,min_day_f33,min_day_f34,min_day_f35,"
    outstr += "min_day_f36,min_day_f37,min_day_f38,min_day_f39,min_day_f40,"
    outstr += "min_day_f41,min_day_f42,min_day_f43,min_day_f44,min_day_f45,"
    outstr += "min_day_f46,min_day_f47,min_day_f48,min_day_f49,min_day_f50,"
    outstr += "min_day_f51,min_day_f52,min_day_f53,min_day_f54,min_day_f55,"
    outstr += "min_day_f56,min_day_f57,min_day_f58,min_day_f59,min_day_f60,"
    outstr += "min_day_f61,min_day_f62,min_day_f63,min_day_f64,min_day_f65,"
    outstr += "min_day_f66,min_day_f67,min_day_f68,min_day_f69,min_day_f70,"
    outstr += "min_day_f71,min_day_f72,min_day_f73,min_day_f74,min_day_f75,"
    outstr += "min_day_f76,min_day_f77,min_day_f78,min_day_f79,min_day_f80,"
    outstr += "min_day_f81,min_day_f82,min_day_f83,min_day_f84,min_day_f85,"
    outstr += "min_day_f86,min_day_f87,min_day_f88,min_day_f89,min_day_f90,"
    outstr += "min_day_f91,min_day_f92,min_day_f93,min_day_f94,min_day_f95,"
    outstr += "min_day_f96,min_day_f97,min_day_f98,min_day_f99,"
    outstr += "min_day_f100,min_day_f101,min_day_f102,"
    outstr += "day_zero_crossings,day_mean_crossings,day_interquartile_range,"
    outstr += "day_skewness,day_kurtosis,"
    outstr += "sig_day_f1,sig_day_f2,sig_day_f3,sig_day_f4,sig_day_f5,"
    outstr += "seg_day_f6,seg_day_f7,seg_day_f8,seg_day_f9,seg_day_f10,"
    outstr += "seg_day_f11,seg_day_f12,seg_day_f13,seg_day_f14,seg_day_f15,"
    outstr += "seg_day_f16,seg_day_f17,seg_day_f18,seg_day_f19,seg_day_f20,"
    outstr += "seg_day_f21,seg_day_f22,seg_day_f23,seg_day_f24,seg_day_f25,"
    outstr += "seg_day_f26,seg_day_f27,seg_day_f28,seg_day_f29,seg_day_f30,"
    outstr += "seg_day_f31,seg_day_f32,seg_day_f33,seg_day_f34,seg_day_f35,"
    outstr += "seg_day_f36,seg_day_f37,seg_day_f38,seg_day_f39,seg_day_f40,"
    outstr += "seg_day_f41,seg_day_f42,seg_day_f43,seg_day_f44,seg_day_f45,"
    outstr += "seg_day_f46,seg_day_f47,seg_day_f48,seg_day_f49,seg_day_f50,"
    outstr += "seg_day_f51,seg_day_f52,seg_day_f53,seg_day_f54,seg_day_f55,"
    outstr += "seg_day_f56,seg_day_f57,seg_day_f58,seg_day_f59,seg_day_f60,"
    outstr += "seg_day_f61,seg_day_f62,seg_day_f63,seg_day_f64,seg_day_f65,"
    outstr += "seg_day_f66,seg_day_f67,seg_day_f68,seg_day_f69,seg_day_f70,"
    outstr += "seg_day_f71,seg_day_f72,seg_day_f73,seg_day_f74,seg_day_f75,"
    outstr += "seg_day_f76,seg_day_f77,seg_day_f78,seg_day_f79,seg_day_f80,"
    outstr += "seg_day_f81,seg_day_f82,seg_day_f83,seg_day_f84,seg_day_f85,"
    outstr += "seg_day_f86,seg_day_f87,seg_day_f88,seg_day_f89,seg_day_f90,"
    outstr += "seg_day_f91,seg_day_f92,seg_day_f93,seg_day_f94,seg_day_f95,"
    outstr += "seg_day_f96,seg_day_f97,seg_day_f98,seg_day_f99,"
    outstr += "seg_day_f100,seg_day_f101,seg_day_f102,"
    outstr += "mean_hour_f1,mean_hour_f2,mean_hour_f3,mean_hour_f4,mean_hour_f5,"
    outstr += "mean_hour_f6,mean_hour_f7,mean_hour_f8,mean_hour_f9,mean_hour_f10,"
    outstr += "mean_hour_f11,mean_hour_f12,mean_hour_f13,mean_hour_f14,"
    outstr += "mean_hour_f15,mean_hour_f16,mean_hour_f17,mean_hour_f18,"
    outstr += "mean_hour_f19,mean_hour_f20,mean_hour_f21,mean_hour_f22,"
    outstr += "mean_hour_f23,mean_hour_f24,mean_hour_f25,mean_hour_f26,"
    outstr += "mean_hour_f27,mean_hour_f28,mean_hour_f29,mean_hour_f30,"
    outstr += "mean_hour_f31,mean_hour_f32,mean_hour_f33,mean_hour_f34,"
    outstr += "mean_hour_f35,mean_hour_f36,mean_hour_f37,mean_hour_f38,"
    outstr += "mean_hour_f39,mean_hour_f40,mean_hour_f41,mean_hour_f42,"
    outstr += "mean_hour_f43,mean_hour_f44,mean_hour_f45,mean_hour_f46,"
    outstr += "mean_hour_f47,mean_hour_f48,mean_hour_f49,mean_hour_f50,"
    outstr += "mean_hour_f51,mean_hour_f52,mean_hour_f53,"
    outstr += "med_hour_f1,med_hour_f2,med_hour_f3,med_hour_f4,med_hour_f5,"
    outstr += "med_hour_f6,med_hour_f7,med_hour_f8,med_hour_f9,med_hour_f10,"
    outstr += "med_hour_f11,med_hour_f12,med_hour_f13,med_hour_f14,med_hour_f15,"
    outstr += "med_hour_f16,med_hour_f17,med_hour_f18,med_hour_f19,med_hour_f20,"
    outstr += "med_hour_f21,med_hour_f22,med_hour_f23,med_hour_f24,med_hour_f25,"
    outstr += "med_hour_f26,med_hour_f27,med_hour_f28,med_hour_f29,med_hour_f30,"
    outstr += "med_hour_f31,med_hour_f32,med_hour_f33,med_hour_f34,med_hour_f35,"
    outstr += "med_hour_f36,med_hour_f37,med_hour_f38,med_hour_f39,med_hour_f40,"
    outstr += "med_hour_f41,med_hour_f42,med_hour_f43,med_hour_f44,med_hour_f45,"
    outstr += "med_hour_f46,med_hour_f47,med_hour_f48,med_hour_f49,med_hour_f50,"
    outstr += "med_hour_f51,med_hour_f52,med_hour_f53,"
    outstr += "std_hour_f1,std_hour_f2,std_hour_f3,std_hour_f4,std_hour_f5,"
    outstr += "std_hour_f6,std_hour_f7,std_hour_f8,std_hour_f9,std_hour_f10,"
    outstr += "std_hour_f11,std_hour_f12,std_hour_f13,std_hour_f14,std_hour_f15,"
    outstr += "std_hour_f16,std_hour_f17,std_hour_f18,std_hour_f19,std_hour_f20,"
    outstr += "std_hour_f21,std_hour_f22,std_hour_f23,std_hour_f24,std_hour_f25,"
    outstr += "std_hour_f26,std_hour_f27,std_hour_f28,std_hour_f29,std_hour_f30,"
    outstr += "std_hour_f31,std_hour_f32,std_hour_f33,std_hour_f34,std_hour_f35,"
    outstr += "std_hour_f36,std_hour_f37,std_hour_f38,std_hour_f39,std_hour_f40,"
    outstr += "std_hour_f41,std_hour_f42,std_hour_f43,std_hour_f44,std_hour_f45,"
    outstr += "std_hour_f46,std_hour_f47,std_hour_f48,std_hour_f49,std_hour_f50,"
    outstr += "std_hour_f51,std_hour_f52,std_hour_f53,"
    outstr += "max_hour_f1,max_hour_f2,max_hour_f3,max_hour_f4,max_hour_f5,"
    outstr += "max_hour_f6,max_hour_f7,max_hour_f8,max_hour_f9,max_hour_f10,"
    outstr += "max_hour_f11,max_hour_f12,max_hour_f13,max_hour_f14,max_hour_f15,"
    outstr += "max_hour_f16,max_hour_f17,max_hour_f18,max_hour_f19,max_hour_f20,"
    outstr += "max_hour_f21,max_hour_f22,max_hour_f23,max_hour_f24,max_hour_f25,"
    outstr += "max_hour_f26,max_hour_f27,max_hour_f28,max_hour_f29,max_hour_f30,"
    outstr += "max_hour_f31,max_hour_f32,max_hour_f33,max_hour_f34,max_hour_f35,"
    outstr += "max_hour_f36,max_hour_f37,max_hour_f38,max_hour_f39,max_hour_f40,"
    outstr += "max_hour_f41,max_hour_f42,max_hour_f43,max_hour_f44,max_hour_f45,"
    outstr += "max_hour_f46,max_hour_f47,max_hour_f48,max_hour_f49,max_hour_f50,"
    outstr += "max_hour_f51,max_hour_f52,max_hour_f53,"
    outstr += "min_hour_f1,min_hour_f2,min_hour_f3,min_hour_f4,min_hour_f5,"
    outstr += "min_hour_f6,min_hour_f7,min_hour_f8,min_hour_f9,min_hour_f10,"
    outstr += "min_hour_f11,min_hour_f12,min_hour_f13,min_hour_f14,min_hour_f15,"
    outstr += "min_hour_f16,min_hour_f17,min_hour_f18,min_hour_f19,min_hour_f20,"
    outstr += "min_hour_f21,min_hour_f22,min_hour_f23,min_hour_f24,min_hour_f25,"
    outstr += "min_hour_f26,min_hour_f27,min_hour_f28,min_hour_f29,min_hour_f30,"
    outstr += "min_hour_f31,min_hour_f32,min_hour_f33,min_hour_f34,min_hour_f35,"
    outstr += "min_hour_f36,min_hour_f37,min_hour_f38,min_hour_f39,min_hour_f40,"
    outstr += "min_hour_f41,min_hour_f42,min_hour_f43,min_hour_f44,min_hour_f45,"
    outstr += "min_hour_f46,min_hour_f47,min_hour_f48,min_hour_f49,min_hour_f50,"
    outstr += "min_hour_f51,min_hour_f52,min_hour_f53,"
    outstr += "hour_zero_crossings,hour_mean_crossings,hour_interquartile_range,"
    outstr += "hour_skewness,hour_kurtosis,"
    outstr += "sig_hour_f1,sig_hour_f2,sig_hour_f3,sig_hour_f4,sig_hour_f5,"
    outstr += "sig_hour_f6,sig_hour_f7,sig_hour_f8,sig_hour_f9,sig_hour_f10,"
    outstr += "sig_hour_f11,sig_hour_f12,sig_hour_f13,sig_hour_f14,sig_hour_f15,"
    outstr += "sig_hour_f16,sig_hour_f17,sig_hour_f18,sig_hour_f19,sig_hour_f20,"
    outstr += "sig_hour_f21,sig_hour_f22,sig_hour_f23,sig_hour_f24,sig_hour_f25,"
    outstr += "sig_hour_f26,sig_hour_f27,sig_hour_f28,sig_hour_f29,sig_hour_f30,"
    outstr += "sig_hour_f31,sig_hour_f32,sig_hour_f33,sig_hour_f34,sig_hour_f35,"
    outstr += "sig_hour_f36,sig_hour_f37,sig_hour_f38,sig_hour_f39,sig_hour_f40,"
    outstr += "sig_hour_f41,sig_hour_f42,sig_hour_f43,sig_hour_f44,sig_hour_f45,"
    outstr += "sig_hour_f46,sig_hour_f47,sig_hour_f48,sig_hour_f49,sig_hour_f50,"
    outstr += "sig_hour_f51,sig_hour_f52,sig_hour_f53,"
    outstr += "ri_ww_f1,ri_wd_f1,ri_bw_f1,"
    outstr += "ri_ww_f2,ri_wd_f2,ri_bw_f2,"
    outstr += "ri_ww_f3,ri_wd_f3,ri_bw_f3,"
    outstr += "cr_hour_f1,cr_hour_f2,cr_hour_f3"
    return outstr


def generate_bcd_header():
    """ Print header line with feature names for behavior change detection values.
    """
    outstr = "change_score,change_significant"
    return outstr


def print_markers(filename, day_values, hour_values, behavior_markers,
                  behavior_change, dm, day, hour, bm, pp):
    """ Save the generated behavior markers to separate files.
    """
    cf = config.Config()
    fullname = os.path.join(cf.datapath, filename)
    if pp:
        outfile = fullname + '.day'
        str_header = generate_day_header()
        np.savetxt(outfile, day_values, delimiter=',', header=str_header)
        outfile = fullname + '.hour'
        str_header = generate_hour_header()
        np.savetxt(outfile, hour_values, delimiter=',', header=str_header)
        outfile = fullname + '.bm'
        str_header = generate_behavior_header()
        np.savetxt(outfile, [behavior_markers], delimiter=',', header=str_header)
        outfile = fullname + '.bcd'
        str_header = generate_bcd_header()
        np.savetxt(outfile, behavior_change, delimiter=',', header=str_header)
    else:
        outfile = fullname + '.bm'
        np.savetxt(outfile, [behavior_markers], delimiter=',')
        outfile = fullname + '.bcd'
        np.savetxt(outfile, behavior_change, delimiter=',')
