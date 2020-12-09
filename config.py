# config.py
# Global variables

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


class Config:

    def __init__(self):
        """ Constructor
        """
        self.date = 0
        self.time = 1
        self.yaw = 2
        self.pitch = 3
        self.roll = 4
        self.x_rotation = 5
        self.y_rotation = 6
        self.z_rotation = 7
        self.x_acceleration = 8
        self.y_acceleration = 9
        self.z_acceleration = 10
        self.latitude = 11
        self.longitude = 12
        self.altitude = 13
        self.course = 14
        self.speed = 15
        self.horizontal_accuracy = 16
        self.vertical_accuracy = 17
        self.num_sensors = 18
        self.oneclass_pos = 18
        self.activity_pos = 51
        self.missing_value_pos = 52
        self.num_activities = 33
        self.num_locations = 4
        self.datapath = './'
        self.minutes_in_day = 1440
        self.translate = False

        # list of activity classes for overall activity
        self.activity_list = ['Chores', 'Eat', 'Entertainment', 'Errands',
                              'Exercise', 'Hobby', 'Hygiene', 'Relax', 'School',
                              'Sleep', 'Travel', 'Work']

    def set_parameters(self, args):
        """ Set parameters according to command-line args list.
        """
        num = len(args)
        index = 1
        while index < (num - 1):
            option = args[index]
            if option == "--datapath":
                index += 1
                self.datapath = args[index]
            elif option == "--activity_list":
                index += 1
                alist = args[index]
                self.activity_list = alist.split(',')
            elif option == "--translate":
                self.translate = True
        return args[1]
