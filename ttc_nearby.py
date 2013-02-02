#!/usr/bin/env python

import json, math

def stopsInRange(longitude, latitude):
    stops = []
    with open('ttc_stops.json') as ttcStops:
        stopJSON = json.load(ttcStops)
        stops = stopJSON['Stops']
    stopsInRange = []
    for stop in stops:
        if(distance([latitude, longitude], [float(stop['lat']), float(stop['lon'])]) < 15422.8):
            stopsInRange.append(stop)
    data = { "NearbyStops" : stopsInRange }
    return data

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

data = json.dumps(stopsInRange(43.67391,-79.28172), indent=2)
with open('ttc_nearby.json', 'a') as ttcStops:
    ttcStops.write(data)
