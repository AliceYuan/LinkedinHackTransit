#!/usr/bin/env python

import json, requests
import xml.etree.ElementTree as ET
from ttc_nearby import getNearbyStops
from ttc_request import requestNextBusData

def getUpcomingDepartures(latitude, longitude):
	departures = []
	nearbyStops = json.loads(getNearbyStops(latitude, longitude))["Stops"]
	for stop in nearbyStops:
		if 'stopId' in stop:
			predictions = requestNextBusData('predictions', 'stopId='+stop["stopId"])
			rootPredictions = ET.fromstring(predictions)
			for predictions in rootPredictions.findall('predictions'):
				if len(predictions.findall('direction')) > 0:
					dictionary = {}
					for direction in predictions.findall('direction'):
						for prediction in direction.findall('prediction'):
							dictionary.update({'route': predictions.attrib["routeTag"], 'stop': predictions.attrib["stopTitle"], 'minutes': prediction.attrib["minutes"]})
							departures.append(dictionary)
	data = { "Departures" : departures }
	return data
