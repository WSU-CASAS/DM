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
    cf = config.Config()
    outstr = "total_rotation,total_acceleration,total_distance,number_missing,"
    outstr += "oc1_time,oc2_time,oc3_time,oc4_time,oc5_time,oc6_time,oc7_time,"
    outstr += "oc8_time,oc9_time,oc10_time,oc11_time,oc12_time,oc13_time,"
    outstr += "oc14_time,oc15_time,oc16_time,oc17_time,oc18_time,oc19_time,"
    outstr += "oc20_time,oc21_time,oc22_time,oc23_time,oc24_time,oc25_time,"
    outstr += "oc26_time,oc27_time,oc28_time,oc29_time,oc30_time,oc31_time,"
    outstr += "oc32_time,oc33_time,"
    anames = cf.activity_list
    for i in range(len(anames)):
        outstr += anames[i] + "_time,"
    outstr += "oc1_first,oc2_first,"
    outstr += "oc3_first,oc4_first,oc5_first,oc6_first,oc7_first,oc8_first,"
    outstr += "oc9_first,oc10_first,oc11_first,oc12_first,oc13_first,"
    outstr += "oc14_first,oc15_first,oc16_first,oc17_first,oc18_first,"
    outstr += "oc19_first,oc20_first,oc21_first,oc22_first,oc23_first,"
    outstr += "oc24_first,oc25_first,oc26_first,oc27_first,oc28_first,"
    outstr += "oc29_first,oc30_first,oc31_first,oc32_first,oc33_first,"
    for i in range(len(anames)):
        outstr += anames[i] + "_first,"
    outstr += "attraction_time,house_time,restaurant_time,"
    outstr += "road_time,service_time,store_time,work_time,other_time,"
    outstr += "attraction_first,house_first,restaurant_first,road_first,"
    outstr += "service_first,store_first,work_first,other_first"
    return outstr


def generate_hour_header():
    """ Print header line with feature names for hour statistics.
    """
    cf = config.Config()
    outstr = "total_rotation,total_acceleration,total_distance,number_missing,"
    outstr += "oc1_time,oc2_time,oc3_time,oc4_time,oc5_time,oc6_time,oc7_time,"
    outstr += "oc8_time,oc9_time,oc10_time,oc11_time,oc12_time,oc13_time,"
    outstr += "oc14_time,oc15_time,oc16_time,oc17_time,oc18_time,oc19_time,"
    outstr += "oc20_time,oc21_time,oc22_time,oc23_time,oc24_time,oc25_time,"
    outstr += "oc26_time,oc27_time,oc28_time,oc29_time,oc30_time,oc31_time,"
    outstr += "oc32_time,oc33_time,"
    anames = cf.activity_list
    for i in range(len(anames)):
        outstr += anames[i] + "_time,"
    outstr += "attraction_time,house_time,"
    outstr += "restaurant_time,road_time,service_time,store_time,work_time,"
    outstr += "other_time"
    return outstr


def generate_behavior_header():
    """ Print header line with feature names for overall behavior statistics.
    """
    outstr = "mean_day_1,mean_day_2,mean_day_3,mean_day_4,mean_day_5,"
    outstr += "mean_day_6,mean_day_7,mean_day_8,mean_day_9,mean_day_10,"
    outstr += "mean_day_11,mean_day_12,mean_day_13,mean_day_14,mean_day_15,"
    outstr += "mean_day_16,mean_day_17,mean_day_18,mean_day_19,mean_day_20,"
    outstr += "mean_day_21,mean_day_22,mean_day_23,mean_day_24,mean_day_25,"
    outstr += "mean_day_26,mean_day_27,mean_day_28,mean_day_29,mean_day_30,"
    outstr += "mean_day_31,mean_day_32,mean_day_33,mean_day_34,mean_day_35,"
    outstr += "mean_day_36,mean_day_37,mean_day_38,mean_day_39,mean_day_40,"
    outstr += "mean_day_41,mean_day_42,mean_day_43,mean_day_44,mean_day_45,"
    outstr += "mean_day_46,mean_day_47,mean_day_48,mean_day_49,mean_day_50,"
    outstr += "mean_day_51,mean_day_52,mean_day_53,mean_day_54,mean_day_55,"
    outstr += "mean_day_56,mean_day_57,mean_day_58,mean_day_59,mean_day_60,"
    outstr += "mean_day_61,mean_day_62,mean_day_63,mean_day_64,mean_day_65,"
    outstr += "mean_day_66,mean_day_67,mean_day_68,mean_day_69,mean_day_70,"
    outstr += "mean_day_71,mean_day_72,mean_day_73,mean_day_74,mean_day_75,"
    outstr += "mean_day_76,mean_day_77,mean_day_78,mean_day_79,mean_day_80,"
    outstr += "mean_day_81,mean_day_82,mean_day_83,mean_day_84,mean_day_85,"
    outstr += "mean_day_86,mean_day_87,mean_day_88,mean_day_89,mean_day_90,"
    outstr += "mean_day_91,mean_day_92,mean_day_93,mean_day_94,mean_day_95,"
    outstr += "mean_day_96,mean_day_97,mean_day_98,mean_day_99,"
    outstr += "mean_day_100,mean_day_101,mean_day_102,"
    outstr += "mean_day_103,mean_day_104,mean_day_105,mean_day_106,mean_day_107,"
    outstr += "mean_day_108,mean_day_109,mean_day_110,"
    outstr += "med_day_1,med_day_2,med_day_3,med_day_4,med_day_5,"
    outstr += "med_day_6,med_day_7,med_day_8,med_day_9,med_day_10,"
    outstr += "med_day_11,med_day_12,med_day_13,med_day_14,med_day_15,"
    outstr += "med_day_16,med_day_17,med_day_18,med_day_19,med_day_20,"
    outstr += "med_day_21,med_day_22,med_day_23,med_day_24,med_day_25,"
    outstr += "med_day_26,med_day_27,med_day_28,med_day_29,med_day_30,"
    outstr += "med_day_31,med_day_32,med_day_33,med_day_34,med_day_35,"
    outstr += "med_day_36,med_day_37,med_day_38,med_day_39,med_day_40,"
    outstr += "med_day_41,med_day_42,med_day_43,med_day_44,med_day_45,"
    outstr += "med_day_46,med_day_47,med_day_48,med_day_49,med_day_50,"
    outstr += "med_day_51,med_day_52,med_day_53,med_day_54,med_day_55,"
    outstr += "med_day_56,med_day_57,med_day_58,med_day_59,med_day_60,"
    outstr += "med_day_61,med_day_62,med_day_63,med_day_64,med_day_65,"
    outstr += "med_day_66,med_day_67,med_day_68,med_day_69,med_day_70,"
    outstr += "med_day_71,med_day_72,med_day_73,med_day_74,med_day_75,"
    outstr += "med_day_76,med_day_77,med_day_78,med_day_79,med_day_80,"
    outstr += "med_day_81,med_day_82,med_day_83,med_day_84,med_day_85,"
    outstr += "med_day_86,med_day_87,med_day_88,med_day_89,med_day_90,"
    outstr += "med_day_91,med_day_92,med_day_93,med_day_94,med_day_95,"
    outstr += "med_day_96,med_day_97,med_day_98,med_day_99,"
    outstr += "med_day_100,med_day_101,med_day_102,"
    outstr += "med_day_103,med_day_104,med_day_105,med_day_106,med_day_107,"
    outstr += "med_day_108,med_day_109,med_day_110,"
    outstr += "std_day_1,std_day_2,std_day_3,std_day_4,std_day_5,"
    outstr += "std_day_6,std_day_7,std_day_8,std_day_9,std_day_10,"
    outstr += "std_day_11,std_day_12,std_day_13,std_day_14,std_day_15,"
    outstr += "std_day_16,std_day_17,std_day_18,std_day_19,std_day_20,"
    outstr += "std_day_21,std_day_22,std_day_23,std_day_24,std_day_25,"
    outstr += "std_day_26,std_day_27,std_day_28,std_day_29,std_day_30,"
    outstr += "std_day_31,std_day_32,std_day_33,std_day_34,std_day_35,"
    outstr += "std_day_36,std_day_37,std_day_38,std_day_39,std_day_40,"
    outstr += "std_day_41,std_day_42,std_day_43,std_day_44,std_day_45,"
    outstr += "std_day_46,std_day_47,std_day_48,std_day_49,std_day_50,"
    outstr += "std_day_51,std_day_52,std_day_53,std_day_54,std_day_55,"
    outstr += "std_day_56,std_day_57,std_day_58,std_day_59,std_day_60,"
    outstr += "std_day_61,std_day_62,std_day_63,std_day_64,std_day_65,"
    outstr += "std_day_66,std_day_67,std_day_68,std_day_69,std_day_70,"
    outstr += "std_day_71,std_day_72,std_day_73,std_day_74,std_day_75,"
    outstr += "std_day_76,std_day_77,std_day_78,std_day_79,std_day_80,"
    outstr += "std_day_81,std_day_82,std_day_83,std_day_84,std_day_85,"
    outstr += "std_day_86,std_day_87,std_day_88,std_day_89,std_day_90,"
    outstr += "std_day_91,std_day_92,std_day_93,std_day_94,std_day_95,"
    outstr += "std_day_96,std_day_97,std_day_98,std_day_99,"
    outstr += "std_day_100,std_day_101,std_day_102,"
    outstr += "std_day_103,std_day_104,std_day_105,std_day_106,std_day_107,"
    outstr += "std_day_108,std_day_109,std_day_110,"
    outstr += "max_day_1,max_day_2,max_day_3,max_day_4,max_day_5,"
    outstr += "max_day_6,max_day_7,max_day_8,max_day_9,max_day_10,"
    outstr += "max_day_11,max_day_12,max_day_13,max_day_14,max_day_15,"
    outstr += "max_day_16,max_day_17,max_day_18,max_day_19,max_day_20,"
    outstr += "max_day_21,max_day_22,max_day_23,max_day_24,max_day_25,"
    outstr += "max_day_26,max_day_27,max_day_28,max_day_29,max_day_30,"
    outstr += "max_day_31,max_day_32,max_day_33,max_day_34,max_day_35,"
    outstr += "max_day_36,max_day_37,max_day_38,max_day_39,max_day_40,"
    outstr += "max_day_41,max_day_42,max_day_43,max_day_44,max_day_45,"
    outstr += "max_day_46,max_day_47,max_day_48,max_day_49,max_day_50,"
    outstr += "max_day_51,max_day_52,max_day_53,max_day_54,max_day_55,"
    outstr += "max_day_56,max_day_57,max_day_58,max_day_59,max_day_60,"
    outstr += "max_day_61,max_day_62,max_day_63,max_day_64,max_day_65,"
    outstr += "max_day_66,max_day_67,max_day_68,max_day_69,max_day_70,"
    outstr += "max_day_71,max_day_72,max_day_73,max_day_74,max_day_75,"
    outstr += "max_day_76,max_day_77,max_day_78,max_day_79,max_day_80,"
    outstr += "max_day_81,max_day_82,max_day_83,max_day_84,max_day_85,"
    outstr += "max_day_86,max_day_87,max_day_88,max_day_89,max_day_90,"
    outstr += "max_day_91,max_day_92,max_day_93,max_day_94,max_day_95,"
    outstr += "max_day_96,max_day_97,max_day_98,max_day_99,"
    outstr += "max_day_100,max_day_101,max_day_102,"
    outstr += "max_day_103,max_day_104,max_day_105,max_day_106,max_day_107,"
    outstr += "max_day_108,max_day_109,max_day_110,"
    outstr += "min_day_1,min_day_2,min_day_3,min_day_4,min_day_5,"
    outstr += "min_day_6,min_day_7,min_day_8,min_day_9,min_day_10,"
    outstr += "min_day_11,min_day_12,min_day_13,min_day_14,min_day_15,"
    outstr += "min_day_16,min_day_17,min_day_18,min_day_19,min_day_20,"
    outstr += "min_day_21,min_day_22,min_day_23,min_day_24,min_day_25,"
    outstr += "min_day_26,min_day_27,min_day_28,min_day_29,min_day_30,"
    outstr += "min_day_31,min_day_32,min_day_33,min_day_34,min_day_35,"
    outstr += "min_day_36,min_day_37,min_day_38,min_day_39,min_day_40,"
    outstr += "min_day_41,min_day_42,min_day_43,min_day_44,min_day_45,"
    outstr += "min_day_46,min_day_47,min_day_48,min_day_49,min_day_50,"
    outstr += "min_day_51,min_day_52,min_day_53,min_day_54,min_day_55,"
    outstr += "min_day_56,min_day_57,min_day_58,min_day_59,min_day_60,"
    outstr += "min_day_61,min_day_62,min_day_63,min_day_64,min_day_65,"
    outstr += "min_day_66,min_day_67,min_day_68,min_day_69,min_day_70,"
    outstr += "min_day_71,min_day_72,min_day_73,min_day_74,min_day_75,"
    outstr += "min_day_76,min_day_77,min_day_78,min_day_79,min_day_80,"
    outstr += "min_day_81,min_day_82,min_day_83,min_day_84,min_day_85,"
    outstr += "min_day_86,min_day_87,min_day_88,min_day_89,min_day_90,"
    outstr += "min_day_91,min_day_92,min_day_93,min_day_94,min_day_95,"
    outstr += "min_day_96,min_day_97,min_day_98,min_day_99,"
    outstr += "min_day_100,min_day_101,min_day_102,"
    outstr += "min_day_103,min_day_104,min_day_105,min_day_106,min_day_107,"
    outstr += "min_day_108,min_day_109,min_day_110,"
    outstr += "day_zero_crossings,day_mean_crossings,day_interquartile_range,"
    outstr += "day_skewness,day_kurtosis,"
    outstr += "sig_day_1,sig_day_2,sig_day_3,sig_day_4,sig_day_5,"
    outstr += "sig_day_6,sig_day_7,sig_day_8,sig_day_9,sig_day_10,"
    outstr += "sig_day_11,sig_day_12,sig_day_13,sig_day_14,sig_day_15,"
    outstr += "sig_day_16,sig_day_17,sig_day_18,sig_day_19,sig_day_20,"
    outstr += "sig_day_21,sig_day_22,sig_day_23,sig_day_24,sig_day_25,"
    outstr += "sig_day_26,sig_day_27,sig_day_28,sig_day_29,sig_day_30,"
    outstr += "sig_day_31,sig_day_32,sig_day_33,sig_day_34,sig_day_35,"
    outstr += "sig_day_36,sig_day_37,sig_day_38,sig_day_39,sig_day_40,"
    outstr += "sig_day_41,sig_day_42,sig_day_43,sig_day_44,sig_day_45,"
    outstr += "sig_day_46,sig_day_47,sig_day_48,sig_day_49,sig_day_50,"
    outstr += "sig_day_51,sig_day_52,sig_day_53,sig_day_54,sig_day_55,"
    outstr += "sig_day_56,sig_day_57,sig_day_58,sig_day_59,sig_day_60,"
    outstr += "sig_day_61,sig_day_62,sig_day_63,sig_day_64,sig_day_65,"
    outstr += "sig_day_66,sig_day_67,sig_day_68,sig_day_69,sig_day_70,"
    outstr += "sig_day_71,sig_day_72,sig_day_73,sig_day_74,sig_day_75,"
    outstr += "sig_day_76,sig_day_77,sig_day_78,sig_day_79,sig_day_80,"
    outstr += "sig_day_81,sig_day_82,sig_day_83,sig_day_84,sig_day_85,"
    outstr += "sig_day_86,sig_day_87,sig_day_88,sig_day_89,sig_day_90,"
    outstr += "sig_day_91,sig_day_92,sig_day_93,sig_day_94,sig_day_95,"
    outstr += "sig_day_96,sig_day_97,sig_day_98,sig_day_99,"
    outstr += "sig_day_100,sig_day_101,sig_day_102,"
    outstr += "sig_day_103,sig_day_104,sig_day_105,sig_day_106,sig_day_107,"
    outstr += "sig_day_108,sig_day_109,sig_day_110,"
    outstr += "mean_hour_1,mean_hour_2,mean_hour_3,mean_hour_4,mean_hour_5,"
    outstr += "mean_hour_6,mean_hour_7,mean_hour_8,mean_hour_9,mean_hour_10,"
    outstr += "mean_hour_11,mean_hour_12,mean_hour_13,mean_hour_14,mean_hour_15,"
    outstr += "mean_hour_16,mean_hour_17,mean_hour_18,mean_hour_19,mean_hour_20,"
    outstr += "mean_hour_21,mean_hour_22,mean_hour_23,mean_hour_24,mean_hour_25,"
    outstr += "mean_hour_26,mean_hour_27,mean_hour_28,mean_hour_29,mean_hour_30,"
    outstr += "mean_hour_31,mean_hour_32,mean_hour_33,mean_hour_34,mean_hour_35,"
    outstr += "mean_hour_36,mean_hour_37,mean_hour_38,mean_hour_39,mean_hour_40,"
    outstr += "mean_hour_41,mean_hour_42,mean_hour_43,mean_hour_44,mean_hour_45,"
    outstr += "mean_hour_46,mean_hour_47,mean_hour_48,mean_hour_49,mean_hour_50,"
    outstr += "mean_hour_51,mean_hour_52,mean_hour_53,"
    outstr += "mean_hour_54,mean_hour_55,mean_hour_56,mean_hour_57,"
    outstr += "med_hour_1,med_hour_2,med_hour_3,med_hour_4,med_hour_5,"
    outstr += "med_hour_6,med_hour_7,med_hour_8,med_hour_9,med_hour_10,"
    outstr += "med_hour_11,med_hour_12,med_hour_13,med_hour_14,med_hour_15,"
    outstr += "med_hour_16,med_hour_17,med_hour_18,med_hour_19,med_hour_20,"
    outstr += "med_hour_21,med_hour_22,med_hour_23,med_hour_24,med_hour_25,"
    outstr += "med_hour_26,med_hour_27,med_hour_28,med_hour_29,med_hour_30,"
    outstr += "med_hour_31,med_hour_32,med_hour_33,med_hour_34,med_hour_35,"
    outstr += "med_hour_36,med_hour_37,med_hour_38,med_hour_39,med_hour_40,"
    outstr += "med_hour_41,med_hour_42,med_hour_43,med_hour_44,med_hour_45,"
    outstr += "med_hour_46,med_hour_47,med_hour_48,med_hour_49,med_hour_50,"
    outstr += "med_hour_51,med_hour_52,med_hour_53,"
    outstr += "med_hour_54,med_hour_55,med_hour_56,med_hour_57,"
    outstr += "std_hour_1,std_hour_2,std_hour_3,std_hour_4,std_hour_5,"
    outstr += "std_hour_6,std_hour_7,std_hour_8,std_hour_9,std_hour_10,"
    outstr += "std_hour_11,std_hour_12,std_hour_13,std_hour_14,std_hour_15,"
    outstr += "std_hour_16,std_hour_17,std_hour_18,std_hour_19,std_hour_20,"
    outstr += "std_hour_21,std_hour_22,std_hour_23,std_hour_24,std_hour_25,"
    outstr += "std_hour_26,std_hour_27,std_hour_28,std_hour_29,std_hour_30,"
    outstr += "std_hour_31,std_hour_32,std_hour_33,std_hour_34,std_hour_35,"
    outstr += "std_hour_36,std_hour_37,std_hour_38,std_hour_39,std_hour_40,"
    outstr += "std_hour_41,std_hour_42,std_hour_43,std_hour_44,std_hour_45,"
    outstr += "std_hour_46,std_hour_47,std_hour_48,std_hour_49,std_hour_50,"
    outstr += "std_hour_51,std_hour_52,std_hour_53,"
    outstr += "std_hour_54,std_hour_55,std_hour_56,std_hour_57,"
    outstr += "max_hour_1,max_hour_2,max_hour_3,max_hour_4,max_hour_5,"
    outstr += "max_hour_6,max_hour_7,max_hour_8,max_hour_9,max_hour_10,"
    outstr += "max_hour_11,max_hour_12,max_hour_13,max_hour_14,max_hour_15,"
    outstr += "max_hour_16,max_hour_17,max_hour_18,max_hour_19,max_hour_20,"
    outstr += "max_hour_21,max_hour_22,max_hour_23,max_hour_24,max_hour_25,"
    outstr += "max_hour_26,max_hour_27,max_hour_28,max_hour_29,max_hour_30,"
    outstr += "max_hour_31,max_hour_32,max_hour_33,max_hour_34,max_hour_35,"
    outstr += "max_hour_36,max_hour_37,max_hour_38,max_hour_39,max_hour_40,"
    outstr += "max_hour_41,max_hour_42,max_hour_43,max_hour_44,max_hour_45,"
    outstr += "max_hour_46,max_hour_47,max_hour_48,max_hour_49,max_hour_50,"
    outstr += "max_hour_51,max_hour_52,max_hour_53,"
    outstr += "max_hour_54,max_hour_55,max_hour_56,max_hour_57,"
    outstr += "min_hour_1,min_hour_2,min_hour_3,min_hour_4,min_hour_5,"
    outstr += "min_hour_6,min_hour_7,min_hour_8,min_hour_9,min_hour_10,"
    outstr += "min_hour_11,min_hour_12,min_hour_13,min_hour_14,min_hour_15,"
    outstr += "min_hour_16,min_hour_17,min_hour_18,min_hour_19,min_hour_20,"
    outstr += "min_hour_21,min_hour_22,min_hour_23,min_hour_24,min_hour_25,"
    outstr += "min_hour_26,min_hour_27,min_hour_28,min_hour_29,min_hour_30,"
    outstr += "min_hour_31,min_hour_32,min_hour_33,min_hour_34,min_hour_35,"
    outstr += "min_hour_36,min_hour_37,min_hour_38,min_hour_39,min_hour_40,"
    outstr += "min_hour_41,min_hour_42,min_hour_43,min_hour_44,min_hour_45,"
    outstr += "min_hour_46,min_hour_47,min_hour_48,min_hour_49,min_hour_50,"
    outstr += "min_hour_51,min_hour_52,min_hour_53,"
    outstr += "min_hour_54,min_hour_55,min_hour_56,min_hour_57,"
    outstr += "hour_zero_crossings,hour_mean_crossings,hour_interquartile_range,"
    outstr += "hour_skewness,hour_kurtosis,"
    outstr += "sig_hour_1,sig_hour_2,sig_hour_3,sig_hour_4,sig_hour_5,"
    outstr += "sig_hour_6,sig_hour_7,sig_hour_8,sig_hour_9,sig_hour_10,"
    outstr += "sig_hour_11,sig_hour_12,sig_hour_13,sig_hour_14,sig_hour_15,"
    outstr += "sig_hour_16,sig_hour_17,sig_hour_18,sig_hour_19,sig_hour_20,"
    outstr += "sig_hour_21,sig_hour_22,sig_hour_23,sig_hour_24,sig_hour_25,"
    outstr += "sig_hour_26,sig_hour_27,sig_hour_28,sig_hour_29,sig_hour_30,"
    outstr += "sig_hour_31,sig_hour_32,sig_hour_33,sig_hour_34,sig_hour_35,"
    outstr += "sig_hour_36,sig_hour_37,sig_hour_38,sig_hour_39,sig_hour_40,"
    outstr += "sig_hour_41,sig_hour_42,sig_hour_43,sig_hour_44,sig_hour_45,"
    outstr += "sig_hour_46,sig_hour_47,sig_hour_48,sig_hour_49,sig_hour_50,"
    outstr += "sig_hour_51,sig_hour_52,sig_hour_53,"
    outstr += "sig_hour_54,sig_hour_55,sig_hour_56,sig_hour_57,"
    outstr += "ri_ww_acc,ri_wd_acc,ri_sun_acc,ri_mon_acc,ri_tue_acc,"
    outstr += "ri_wed_acc,ri_thu_acc,ri_fri_acc,ri_sat_acc,"
    outstr += "ri_ww_rot,ri_wd_rot,ri_sun_rot,ri_mon_rot,ri_tue_rot,"
    outstr += "ri_wed_rot,ri_thu_rot,ri_fri_rot,ri_sat_rot,"
    outstr += "ri_ww_dist,ri_wd_dist,ri_sun_dist,ri_mon_dist,ri_tue_dist,"
    outstr += "ri_wed_dist,ri_thu_dist,ri_fri_dist,ri_sat_dist,"
    outstr += "cr_hour_1,cr_hour_2,cr_hour_3"
    return outstr


def generate_bcd_header():
    """ Print header line with feature names for behavior change detection values.
    """
    outstr = "change_score,change_significant"
    return outstr


def print_markers(filename, day_values, hour_values, behavior_markers, \
                  behavior_change, dm, day, hour, bm, pp):
    """ Save the generated behavior markers to separate files.
    """
    cf = config.Config()
    fullname = os.path.join(cf.datapath, filename)
    if pp == True:
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


def main():
    print(generate_day_header())
    print(generate_hour_header())
    print(generate_behavior_header())
    print(generate_bcd_header())


if __name__ == "__main__":
    main()
