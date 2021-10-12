#!/usr/bin/python

# python Location.py <data_file>
#
# Performs location type learning on the given data file and outputs either the
# learned model, or the confusion matrices and accuracy for a 3-fold
# cross-validation test.
#
# Requires files: l.translate, locations

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import math
import os.path
import sys

import joblib
import numpy
from numpy import mean
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

import features
import gps
import utils


class Location:

    def __init__(self, filename=None):
        """ Constructor
        """
        self.lmappings = dict()
        self.lmappings['other'] = 'other'
        if filename is None:
            self.infile = "locations"
        else:
            self.infile = filename
        self.locations = list()
        self.local = 1  # Use the local GPS values
        self.cross_validation = 0  # cross validation
        self.xdata = list()
        self.ydata = list()
        self.numseconds = 5  # Number of seconds of data to include in sequence
        self.samplerate = 1  # Number of samples per second
        self.samplesize = self.numseconds * self.samplerate
        self.clf = RandomForestClassifier(n_estimators=50, bootstrap=True,
                                          criterion="entropy", class_weight="balanced", max_depth=5)

    @staticmethod
    def read_entry(infile):
        """ Parse a single line from a text file containing a sensor reading.
        The format is "date time sensorname sensorname value <activitylabel|0>".
        """
        try:
            line = infile.readline()
            x = str(str(line).strip()).split(' ', 5)
            if len(x) < 6:
                return True, x[0], x[1], x[2], x[3], x[4], 'None'
            else:
                x[5] = x[5].replace(' ', '_')
                return True, x[0], x[1], x[2], x[3], x[4], x[5]
        except:
            return False, None, None, None, None, None, None

    def map_location_name(self, name):
        """ Return the location type that is associated with a specific location
        name, using the stored list of location mappings.
        """
        newname = self.lmappings.get(name)
        if newname is None:
            return 'other'
        else:
            return newname

    @staticmethod
    def generate_location_num(name):
        """ Transform a location type into an index value.
        """
        if name == 'attraction':
            return 0
        if name == 'house':
            return 1
        elif name == 'restaurant':
            return 2
        elif name == 'road':
            return 3
        elif name == 'service':
            return 4
        elif name == 'store':
            return 5
        elif name == 'work':
            return 6
        else:
            return 7

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

    def read_locations(self):
        """ Read and store list of locations and corresponding location types.
        This function assumes that file locations exists in the same directory
        as the code. File locations contains an arbitrary number of lines, each
        with syntax "latitude longitude type1 type2 type3". Open street maps
        return as many as three location types associated with a lat,long
        location. They can provide alternate type names or levels of abstraction.
        In this function, only the first type is stored with the latitude
        and longitude.
        """
        read_locations_index = 0
        with open('locations', "r") as file:
            for line in file:
                x = str(str(line).strip()).split(' ', 3)
                triple = list()
                triple.append(float(x[0]))
                triple.append(float(x[1]))
                triple.append(x[2])
                self.locations.append(triple)
                read_locations_index = read_locations_index + 1
        return read_locations_index

    def find_location(self, latitude, longitude):
        """ Determine whether the input location is close (within a threshold
        distance) to the locations already stored in the external list.
        """
        threshold = 0.005
        for triple in self.locations:
            tlat = triple[0]
            tlong = triple[1]
            dist = math.sqrt(((tlat - latitude) * (tlat - latitude)) +
                             ((tlong - longitude) * (tlong - longitude)))
            if dist < threshold:
                return triple[2]
        return None

    def generate_gps_features(self, latitude, longitude):
        """ Generate location features.
        """
        location = self.find_location(latitude, longitude)
        if location is not None:
            return location
        else:
            location = list()
            location.append(latitude)
            location.append(longitude)
            gps_type = gps.get_location_type(location, 'locations')
            location.append(gps_type)
            self.locations.append(location)
            return gps_type

    def extract_features(self, infile):
        """ Extract a feature vector that will be input to a location classifier.
        """
        fs1 = list()
        fs2 = list()
        if not os.path.isfile(infile):
            print(infile, "does not exist")
            exit()

        # process input file for remaining feature vector
        feature_datafile = open(infile, "r")
        count = 0
        valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
        prevdt = utils.get_datetime(date, feature_time)
        temp = 0
        gen = 0
        i = 0
        yaw = list()
        pitch = list()
        roll = list()
        rotx = list()
        roty = list()
        rotz = list()
        accx = list()
        accy = list()
        accz = list()
        acctotal = list()
        latitude = list()
        longitude = list()
        alt = list()
        course = list()
        speed = list()
        hacc = list()
        vacc = list()
        minlat = list()
        maxlat = list()
        minlong = list()
        maxlong = list()
        prevlabel = '0'
        while valid:
            dt = utils.get_datetime(date, feature_time)
            delta = dt - prevdt
            if (delta.seconds > 2) or (gen == 1) or \
                    (delta.seconds < 0) or ((count % self.samplesize) == 0):
                gen = 0
                i = 0
                yaw = list()
                pitch = list()
                roll = list()
                rotx = list()
                roty = list()
                rotz = list()
                accx = list()
                accy = list()
                accz = list()
                acctotal = list()
                latitude = list()
                longitude = list()
                alt = list()
                course = list()
                speed = list()
                hacc = list()
                vacc = list()
                minlat = list()
                maxlat = list()
                minlong = list()
                maxlong = list()
            # first line already read
            yaw.append(utils.clean(float(v1), -1.6, 1.6))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            pitch.append(utils.clean(float(v1), -1.6, 1.6))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            roll.append(utils.clean(float(v1), -1.6, 1.6))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            rotx.append(float(v1))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            roty.append(float(v1))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            rotz.append(float(v1))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            v1 = utils.clean(float(v1), -1.0, 1.0)
            accx.append(v1)
            temp = v1 * v1
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            v1 = utils.clean(float(v1), -1.0, 1.0)
            accy.append(v1)
            temp += v1 * v1
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            v1 = utils.clean(float(v1), -1.0, 1.0)
            accz.append(v1)
            temp += v1 * v1

            # compute combined accuracy
            temp = numpy.sqrt(temp)
            acctotal.append(temp)

            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            latitude.append(float(v1))
            if not minlat:
                minlat = float(v1)
            elif float(v1) < minlat:
                minlat = float(v1)
            if not maxlat:
                maxlat = float(v1)
            elif float(v1) > maxlat:
                maxlat = float(v1)
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            longitude.append(float(v1))
            if not minlong:
                minlong = float(v1)
            elif float(v1) < minlong:
                minlong = float(v1)
            if not maxlong:
                maxlong = float(v1)
            elif float(v1) > maxlong:
                maxlong = float(v1)
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            alt.append(float(v1))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            course.append(float(v1))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            speed.append(float(v1))
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
            hacc.append(float(v1))
            pdt = utils.get_datetime(date, feature_time)
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)

            # Handle case where last VerticalAcc value missing
            if not valid:
                dt = pdt
                v2 = None
                vacc.append(0.0)
            else:
                vacc.append(float(v1))
                dt = utils.get_datetime(date, feature_time)
            month = dt.month
            dayofweek = dt.weekday()
            hours = dt.hour
            minutes = (dt.hour * 60) + dt.minute
            seconds = (dt.hour * 3600) + (dt.minute * 60) + dt.second
            distance = math.sqrt(((maxlat - minlat) * (maxlat - minlat)) +
                                 ((maxlong - minlong) * (maxlong - minlong)))

            hcr = features.heading_change_rate(course, distance)
            sr = features.stop_rate(latitude, longitude, distance)
            trajectory = features.trajectory(latitude, longitude)
            if (count % self.samplesize) == 0:
                xpoint = list()
                gen = 1
                for i in [yaw, pitch, roll, rotx, roty, rotz,
                          accx, accy, accz, acctotal]:
                    while len(i) > self.samplesize:  # remove elements ouside window
                        del i[0]
                    xpoint.extend(features.generate_statistical_features(i))
                if self.local == 1:
                    for i in [latitude, longitude, alt]:
                        xpoint.extend(features.generate_statistical_features(i))
                    for i in [course, speed, hacc, vacc]:
                        xpoint.extend(features.generate_statistical_features(i))
                    xpoint.append(distance)
                    xpoint.append(hcr)
                    xpoint.append(sr)
                    xpoint.append(trajectory)
                xpoint.append(month)
                xpoint.append(dayofweek)
                xpoint.append(hours)
                xpoint.append(minutes)
                xpoint.append(seconds)

                place = self.generate_gps_features(mean(latitude), mean(longitude))

                if place != 'None':
                    self.xdata.append(xpoint)
                    yvalue = self.map_location_name(place)
                    self.ydata.append(yvalue)
            else:
                i += 1
            if not valid:
                prevdt = pdt
            else:
                prevdt = utils.get_datetime(date, feature_time)
            count += 1
            if (count % 100000) == 0:
                print('count', count)
            valid, date, feature_time, f1, f2, v1, v2 = self.read_entry(feature_datafile)
        feature_datafile.close()

    def label_loc(self, clf, yaw, pitch, roll, rotx, roty, rotz, accx, accy, accz,
                  acctotal, latitude, longitude, alt, course, speed, hacc, vacc,
                  distance, hcr, sr, trajectory,
                  month, dayofweek, hours, minutes, seconds):
        """ Use the pretrained location classifier to extract features from the
        input sensor values and map the feature vector onto a location type.
        """
        xpoint = list()
        for i in [yaw, pitch, roll, rotx, roty, rotz, accx, accy, accz, acctotal]:
            xpoint.extend(features.generate_statistical_features(i))
        for i in [latitude, longitude, alt]:
            xpoint.extend(features.generate_statistical_features(i))
        for i in [course, speed, hacc, vacc]:
            xpoint.extend(features.generate_statistical_features(i))
        xpoint.append(distance)
        xpoint.append(hcr)
        xpoint.append(sr)
        xpoint.append(trajectory)
        xpoint.append(month)
        xpoint.append(dayofweek)
        xpoint.append(hours)
        xpoint.append(minutes)
        xpoint.append(seconds)
        self.xdata = [xpoint]
        labels = self.clf.predict(self.xdata)
        return labels[0]

    def train_location_model(self):
        """ Train a model to map a feature vector (statistical operations
        applied to sensor values and raw location values) onto a location type.
        """
        aset = set(self.ydata)
        if self.cross_validation > 0:  # k-fold cross validation
            for i in range(self.cross_validation):
                numright = 0
                total = 0
                xtrain, xtest, ytrain, ytest = train_test_split(self.xdata,
                                                                self.ydata,
                                                                test_size=0.33,
                                                                random_state=i)
                self.clf.fit(xtrain, ytrain)
                newlabels = self.clf.predict(xtest)
                print('newlabels', newlabels)
                matrix = confusion_matrix(ytest, newlabels)
                print('matrix', matrix)
                for j in range(len(ytest)):
                    if newlabels[j] == ytest[j]:
                        numright += 1
                total += 1
                print('accuracy', float(numright) / float(total))
        else:  # store the learned model
            self.clf.fit(self.xdata, self.ydata)
            outstr = "locmodel.pkl"
            joblib.dump(self.clf, outstr)

    @staticmethod
    def load_location_model(modelfilename):
        """ Load a pretrained model that maps a feature vector
        (statistical operations applied to sensor values and raw location values)
        onto a location type.
        """
        filename = "locmodel.pkl"
        clf = joblib.load(filename)
        return clf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply a file of locations")
        exit()
    loc = Location(sys.argv[1])
    loc.read_location_mappings()
    locations_index = loc.read_locations()
    if len(sys.argv) > 2:
        datafile = sys.argv[2]
        loc.extract_features(datafile)
        loc.train_location_model()
