#!/usr/bin/env python

import json, math

def getNearbyStops(latitude, longitude, distance):
    stops = []
    with open('ttc_stops.json') as ttcStops:
        stopJSON = json.load(ttcStops)
        stops = stopJSON['Stops']
    stopsInRange = []
    for stop in stops:
        if(distance([latitude, longitude], [float(stop['lat']), float(stop['lon'])]) <= distance):
            stopsInRange.append(stop)
    nearbyStops = { "NearbyStops" : stopsInRange }
    return nearbyStops

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
    * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d
