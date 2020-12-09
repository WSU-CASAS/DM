#!/usr/bin/python

# Looks up location type information for each unique GPS coordinate in the
# <gps_coord_file>, starting from line <start_line>, and writes the information
# to the locations file. If locations file already exists, then it first reads
# all the previous location information. This file is then over-written with
# both the old and new information.

# Written by Diane J. Cook, Washington State University.

# Copyright (c) 2020. Washington State University (WSU). All rights reserved.
# Code and data may not be used or distributed without permission from WSU.


import math
import sys
from operator import itemgetter

from geopy.geocoders import Nominatim

# global variables
gps_locations = list()

geolocator = Nominatim(user_agent='DM')


def get_address(adr_loc):
    lat = adr_loc[0]
    long = adr_loc[1]
    location_str = str(str(lat) + ", " + str(long))
    # time.sleep(1)
    try:
        location_obj = geolocator.reverse(location_str)
        astr = str(location_obj.raw)
        return location_obj.address
    except:
        return 'None'


def is_house(lt, classname):
    if lt == 'house' or classname == 'house' or \
            lt == 'hamlet' or classname == 'hamlet' or \
            lt == 'hotel' or classname == 'hotel' or \
            lt == 'motel' or classname == 'motel' or \
            lt == 'camp_site' or lt == 'neighborhood' or \
            lt == 'neighbourhood' or lt == 'retirement_home' or \
            lt == 'residential' or classname == 'residential' or \
            lt == 'private_residence' or lt == 'suburb' or \
            lt == 'nursing_home' or lt == 'neighbourhood':
        return True
    else:
        return False


def is_restaurant(lt, classname):
    if lt == 'bar' or classname == 'bar' or \
            lt == 'restaurant' or classname == 'restaurant' or \
            lt == 'bakery' or classname == 'bakery' or \
            lt == 'bbq' or classname == 'bbq' or \
            lt == 'brewery' or classname == 'brewery' or \
            lt == 'alcohol' or classname == 'alcohol' or \
            lt == 'cafe' or lt == 'coffee' or \
            lt == 'pub' or classname == 'pub' or \
            lt == 'fast_food' or classname == 'fast_food' or \
            lt == 'biergarten' or lt == 'confectionery' or \
            lt == 'food' or lt == 'food_court' or \
            lt == 'seafood' or lt == 'seafood' or \
            lt == 'deli;convenience' or lt == 'nightclub':
        return True
    else:
        return False


def is_road(lt, classname):
    if lt == 'highway' or classname == 'highway' or \
            lt == 'motorway' or classname == 'motorway' or \
            lt == 'motorway_junction' or classname == 'motorway_junction' or \
            lt == 'motorway_link' or classname == 'motorway_link' or \
            lt == 'parking' or classname == 'parking' or \
            lt == 'parking_entrance' or lt == 'parking_space' or \
            lt == 'bus_stop' or classname == 'bus_stop' or \
            lt == 'ferry_terminal' or lt == 'motorcycle' or \
            lt == 'cycleway' or classname == 'cycleway' or \
            lt == 'footway' or classname == 'footway' or \
            lt == 'fuel' or classname == 'fuel' or \
            lt == 'trunk' or classname == 'trunk' or \
            lt == 'road' or classname == 'road' or \
            lt == 'pedestrian' or lt == 'rest_area' or \
            lt == 'terminal' or classname == 'terminal' or \
            classname == 'railway' or lt == 'water' or \
            lt == 'hangar' or lt == 'taxi_way' or \
            lt == 'track' or lt == 'primary' or \
            lt == 'secondary' or lt == 'tertiary' or \
            lt == 'bus_station' or lt == 'bridge':
        return True
    else:
        return False


def is_store(lt, classname):
    if lt == 'bank' or classname == 'bank' or \
            lt == 'bureau_de_change' or classname == 'bureau_de_change' or \
            lt == 'gold_exchange' or lt == 'watches' or \
            lt == 'bicycle_rental' or classname == 'bicycle_rental' or \
            lt == 'bicycle_repair_station' or classname == 'bicycle_repair_station' or \
            lt == 'boutique' or classname == 'boutique' or \
            lt == 'art' or classname == 'art' or lt == 'gallery' or \
            lt == 'art_class' or classname == 'art_class' or \
            lt == 'auto_parts' or classname == 'auto_parts' or \
            lt == 'beauty' or classname == 'beauty' or \
            lt == 'beauty_supply' or classname == 'beauty_supply' or \
            lt == 'books' or classname == 'books' or \
            lt == 'furniture' or classname == 'car_wash' or \
            lt == 'shop' or classname == 'shop' or \
            lt == 'supermarket' or classname == 'supermarket' or \
            lt == 'greengrocer' or lt == 'ice_cream' or \
            lt == 'marketplace' or lt == 'video' or \
            lt == 'clothes' or classname == 'clothes' or \
            lt == 'insurance' or classname == 'insurance' or \
            lt == 'interior_decoration' or \
            lt == 'marketplace' or classname == 'marketplace' or \
            lt == 'atm' or lt == 'insurance' or \
            lt == 'pharmacy' or lt == 'nutrition_supplements' or \
            lt == 'department_store' or lt == 'store' or \
            lt == 'electronics' or lt == 'garden_centre' or \
            lt == 'jewelry' or lt == 'retail' or lt == 'mall' or \
            lt == 'toys' or lt == 'tuxedo' or lt == 'soap' or \
            lt == 'marketplace' or lt == 'variety_store' or \
            lt == 'doityouself':
        return True
    else:
        return False


def is_work(lt, classname):
    if lt == 'office' or classname == 'office' or \
            lt == 'school' or classname == 'school' or \
            lt == 'yes' or classname == 'yes' or \
            lt == 'accountant' or classname == 'accountant' or \
            lt == 'administrative' or classname == 'administrative' or \
            lt == 'government' or lt == 'lawyer' or \
            lt == 'public_building' or classname == 'building' or \
            lt == 'company' or classname == 'public_building' or \
            lt == 'kindergarten' or lt == 'university' or \
            lt == 'conference_center' or lt == 'college':
        return True
    else:
        return False


def is_attraction(lt, classname):
    if lt == 'golf_course' or classname == 'golf_course' or \
            lt == 'aerodrome' or classname == 'aerodrome' or \
            lt == 'attraction' or classname == 'attraction' or \
            lt == 'beach' or classname == 'beach' or \
            lt == 'garden' or classname == 'leisure' or \
            lt == 'tourism' or classname == 'tourism' or \
            lt == 'museum' or classname == 'museum' or \
            lt == 'theatre' or classname == 'theatre' or \
            lt == 'swimming_area' or lt == 'swimming_pool' or \
            lt == 'casino' or lt == 'cinema' or \
            lt == 'park' or classname == 'park' or \
            lt == 'lifeguard_tower' or lt == 'nature_reserve' or \
            lt == 'picnic_site' or lt == 'playground' or \
            lt == 'boat' or classname == 'boat' or \
            lt == 'river' or classname == 'river' or \
            lt == 'social_facility' or classname == 'social_facility' or \
            lt == 'sports_centre' or lt == 'stadium' or \
            lt == 'bench' or classname == 'bench':
        return True
    else:
        return False


def is_service(lt, classname):
    if lt == 'place_of_worship' or classname == 'place_of_worship' or \
            lt == 'fire_station' or classname == 'fire_station' or \
            lt == 'ranger_station' or classname == 'ranger_station' or \
            lt == 'fitness_centre' or lt == 'florist' or \
            lt == 'atm' or classname == 'atm' or \
            lt == 'townhall' or classname == 'townhall' or \
            lt == 'aeroway' or classname == 'aeroway' or \
            lt == 'car_wash' or lt == 'service' or classname == 'service' or \
            lt == 'hospital' or classname == 'hospital' or \
            lt == 'caravan_site' or lt == 'caterer' or \
            lt == 'clinic' or \
            lt == 'community_centre' or lt == 'artwork' or \
            lt == 'dentist' or lt == 'amenity' or \
            classname == 'historic' or lt == 'toilets' or \
            lt == 'post_box' or classname == 'emergency' or \
            lt == 'emissions_testing' or lt == 'library' or \
            lt == 'doctor' or lt == 'doctors' or lt == 'clinic' or \
            lt == 'dry_cleaning' or lt == 'optician' or \
            lt == 'doctors' or lt == 'shelter' or \
            lt == 'post_office' or lt == 'post_box' or \
            classname == 'landuse' or lt == 'car_rental' or \
            lt == 'car_repair' or lt == 'charging_station' or \
            classname == 'natural' or lt == 'books' or \
            lt == 'police' or lt == 'vending_machine' or \
            lt == 'veterinary' or lt == 'charging_station' or \
            lt == 'childcare' or lt == 'gym' or \
            lt == 'auto_repair' or \
            lt == 'tanning' or lt == 'car_sales' or \
            lt == 'car_sales' or lt == 'townhall' or \
            lt == 'compressed_air' or lt == 'chiropractor' or \
            lt == 'recycling' or lt == 'tutoring' or \
            lt == 'employment_agency' or lt == 'estate_agent' or \
            lt == 'realtor' or classname == 'realtor' or \
            lt == 'hunting_stand':
        return True
    else:
        return False


def print_features(latitude, longitude, gpstype, classname):
    global gps_locations

    feature_tuple = list()
    feature_tuple.append(float(latitude))
    feature_tuple.append(float(longitude))
    if is_house(gpstype, classname):
        feature_tuple.append('home')
    elif is_restaurant(gpstype, classname):
        feature_tuple.append('restaurant')
    elif is_road(gpstype, classname):
        feature_tuple.append('road')
    elif is_store(gpstype, classname):
        feature_tuple.append('store')
    elif is_work(gpstype, classname):
        feature_tuple.append('work')
    elif is_attraction(gpstype, classname):
        feature_tuple.append('attraction')
    elif is_service(gpstype, classname):
        feature_tuple.append('service')
    else:
        feature_tuple.append('other')
    feature_tuple.append(gpstype)
    feature_tuple.append(classname)
    print(feature_tuple)
    gps_locations.append(feature_tuple)


def gps_read_locations(lfile):
    global gps_locations

    with open(lfile, "r") as file:
        for line in file:
            x = str(str(line).strip()).split(' ', 4)
            gps_tuple = list()
            gps_tuple.append(float(x[0]))
            gps_tuple.append(float(x[1]))
            gps_tuple.append(x[2])
            gps_tuple.append(x[3])
            gps_tuple.append(x[4])
            gps_locations.append(gps_tuple)


def gps_find_location(lat, long):
    for gps_tuple in gps_locations:
        lat1 = float(lat)
        long1 = float(long)
        tlat = gps_tuple[0]
        tlong = gps_tuple[1]
        dist = math.sqrt(((tlat - lat1) * (tlat - lat1)) + ((tlong - long1) * (tlong - long1)))
        if dist < .005:
            return gps_tuple[2]
    return None


def update_locations(locations, locationsfile):
    locations = sorted(locations, key=itemgetter(0))
    unique_locations = []
    output = open(locationsfile, "w")
    for location in locations:
        if len(location) > 4:
            if location not in unique_locations:
                output.write(str(location[0]) + ' ')
                output.write(str(location[1]) + ' ')
                output.write(location[2] + ' ')
                output.write(location[3] + ' ')
                output.write(location[4] + '\n')
        unique_locations.append(location)
    output.close()


def get_location_type(location, locationsfile):
    description = 'None'

    address = get_address(location)
    if address == 'None' or address is None:
        return 'Other'
    description = geolocator.geocode(address, timeout=None)
    if description == 'None' or description is None:
        return 'Other'
    else:
        raw = description.raw
        lt = raw['type']
        if lt == 'other' or lt == 'Other':
            return lt
        else:
            gps_read_locations(locationsfile)
            # update_locations(gps_locations, locationsfile)
            return lt


# python gps.py temp 0
if __name__ == "__main__":
    if len(sys.argv) > 1:
        infile = sys.argv[1]  # file with lat/long values
    else:
        infile = "latlong"
    if len(sys.argv) > 2:
        start = int(sys.argv[2])  # start position in the file
    else:
        start = 0
    if len(sys.argv) > 3:
        locationsfile = sys.argv[3]
    else:
        locationsfile = "locations"
    gps_read_locations(locationsfile)

    description = ""
    features = 1  # print high-level features
    timeouterror = 0

    inputfile = open(infile, "r")
    if len(sys.argv) > 4:
        end = int(sys.argv[4])
    else:
        end = 10000000
    count = 0
    for line in inputfile:
        if (count >= start) and (count <= end):
            location = str(str(line).strip()).split(' ', 2)
            print('location ', location, 'count', count)
            loc = gps_find_location(location[0], location[1])  # look in file
            if loc is None:
                address = get_address(location)
                try:
                    description = geolocator.geocode(address, timeout=None)
                except:
                    timeouterror = 1
                    print('Error, geocode failed')
                if timeouterror == 0:
                    if address == 'None' or description == 'None' or description is None:
                        print_features(location[0], location[1], 'other', 'other')
                    else:
                        raw = description.raw
                        if features == 1:
                            print_features(location[0], location[1],
                                           raw['type'], raw['class'])
                        else:
                            print(raw['type'], ' ', raw['class'])
        if timeouterror == 0:
            count += 1
        else:
            timeouterror = 0
    inputfile.close()
    update_locations(gps_locations, locationsfile)
