#!/usr/bin/env python

import json, requests
import xml.etree.ElementTree as ET
from ttc_nearby import getNearbyStops
from ttc_request import requestNextBusData

def getUpcomingDepartures(latitude, longitude):
	departures = []
	nearbyStops = json.loads(getNearbyStops(latitude, longitude))["Stops"]
	for stop in nearbyStops:
		dictionary = {}
		if 'stopId' in stop:
			predictions = requestNextBusData('predictions', 'stopId='+stop["stopId"])
			# print predictions
			rootPredictions = ET.fromstring(predictions)
			for predictions in rootPredictions.findall('predictions'):
				if len(predictions.findall('direction')) > 0:
					for direction in predictions.findall('direction'):
						for prediction in direction.findall('prediction'):
							dictionary.update({'route': predictions.attrib["routeTag"], 'stop': predictions.attrib["stopTitle"], 'minutes': prediction.attrib["minutes"]})
				else:
					dictionary.update(predictions.attrib)
		departures.append(dictionary)
	data = { "Departures" : departures }
	return data
