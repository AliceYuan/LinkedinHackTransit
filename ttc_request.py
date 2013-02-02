#!/usr/bin/env python

import json, math, requests
import xml.etree.ElementTree as ET

def requestNextBusData(commandName, params):
	base_url = 'http://webservices.nextbus.com/service/publicXMLFeed'
	agencyTag = 'ttc'
	request_url = base_url + '?' + 'command=' + commandName + '&' + 'a=' + agencyTag + '&' + params
	result = requests.get(request_url).text
	return result

def getNearbyStops(latitude, longitude):
	stops = []
	distances = []
	with open('data/ttc_stops.json') as ttcStops:
		stopJSON = json.load(ttcStops)
		stops = stopJSON["Stops"]
	for stop in stops:
		distances.append(distance([latitude, longitude], [float(stop[2]), float(stop[3])]))
	stops = [stops for (distances, stops) in sorted(zip(distances, stops))]
	stopsJSON = { "Stops" : stops }
	return json.dumps(stopsJSON, indent=2)

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

def getRoutes():
	routes = requestNextBusData('routeList', 'r=')
	rootRoutelist = ET.fromstring(routes)
	routeList = []
	for route in rootRoutelist:
		routeList.append(route.attrib)
	routeJSON = { "Routes" : routeList }
	with open('data/ttc_routes.json', 'w') as ttcRoutes:
		ttcRoutes.write(json.dumps(routeJSON, indent=2))

def getStops():
	stopList = []
	with open('data/ttc_routes.json') as ttcRoutes:
		routeList = json.load(ttcRoutes)["Routes"]
	for route in routeList:
		currentRoute = requestNextBusData('routeConfig', 'r='+route["tag"]+'&terse')
		rootCurrentRoute = ET.fromstring(currentRoute)
		for route in rootCurrentRoute.findall('route'):
			for stop in route.findall('stop'):
				stopList.append((stop.attrib["tag"], route.attrib["tag"], stop.attrib["lat"], stop.attrib["lon"]))
	stopJSON = { "Stops" : stopList }
	with open('data/ttc_stops.json', 'w') as ttcStops:
		ttcStops.write(json.dumps(stopJSON, indent=2))

def getPredictions(latitude, longitude):
	predictionList = []
	numPredictions = 0
	check = False
	dictionary = {}
	nearbyStops = json.loads(getNearbyStops(latitude, longitude))["Stops"]
	for stop in nearbyStops:
		if check:
			break
		predictions = requestNextBusData('predictions', 'r='+stop[1]+'&s='+stop[0])
		rootPredictions = ET.fromstring(predictions)
		for predictions in rootPredictions.findall('predictions'):
			if check:
				break
			if 'dirTitleBecauseNoPredictions' not in predictions.attrib:
				numPredictions += 1
				if(numPredictions == 11):
					check = True
					break
				for direction in predictions.findall('direction'):
					minutes = []
					for prediction in direction.findall('prediction'):
						minutes.append(prediction.attrib["minutes"])
					if predictions.attrib["routeTag"] + direction.attrib["title"] not in dictionary:
						predictionList.append((predictions.attrib["stopTag"], predictions.attrib["routeTag"], stop[2], stop[3], predictions.attrib["stopTitle"], direction.attrib["title"], minutes))
						dictionary[predictions.attrib["routeTag"] + direction.attrib["title"]] = 1
					else:
						numPredictions -= 1
	predictionJSON = { "Predictions" : predictionList }
	return json.dumps(predictionJSON, indent=2)

if __name__=="__main__":
	print getPredictions(43.7739, -79.41427)
	# getRoutes()
	# getStops()
