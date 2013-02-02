#!/usr/bin/env python

import json
import math
import operator
import urllib2
import simplejson

def getNearbyStops(latitude, longitude):
    stops = []
    distances = []
    with open('ttc_stops.json') as ttcStops:
        stopJSON = json.load(ttcStops)
        stops = stopJSON['Stops']
    for stop in stops:
        distances.append(distance([latitude, longitude], [float(stop['lat']), float(stop['lon'])]))
    stops = [stops for (distances, stops) in sorted(zip(distances, stops))]
    data = { "Stops" : stops[:5] }
    return json.dumps(data)

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

def convertToAddress(latitude, longitude){
    request = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+latitude+","+longitude+"&sensor=false"
    file = opener.open(request)
    jsonFile = simplejson.load(file)
    results = jsonFile["results"]
    firstResult = results[0]
    address = firstResult["formatted_address"]
    return address
}