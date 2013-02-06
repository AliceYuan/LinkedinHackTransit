#!/usr/bin/env python

import json, math, requests, time
from bs4 import BeautifulSoup
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
	soup = BeautifulSoup(routes, 'xml')
	rootRoutelist = soup.body.find_all('route')
	routeList = []
	for route in rootRoutelist:
		routeList.append({'routeTag': route['tag'], 'routeTitle': route['title']})
	routeJSON = { 'routes' : routeList }
	return json.dumps(routeJSON, indent=2)

def getStops():
	stopList = []
	with open('data/ttc_routes.json') as ttcRoutes:
		routeList = json.load(ttcRoutes)['routes']
	for route in routeList:
		currentRoute = requestNextBusData('routeConfig', 'r='+route['routeTag']+'&terse')
		soup = BeautifulSoup(currentRoute, 'xml')
		rootCurrentRoute = soup.route.find_all('stop', recursive=False)
		for stop in rootCurrentRoute:
			stopList.append({'routeTag': soup.route['tag'], 'routeTitle': soup.route['title'], 'stopTag': stop['tag'], 'lat': stop['lat'], 'lon': stop['lon']})
	stopJSON = { 'stops' : stopList }
	return json.dumps(stopJSON, indent=2)

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

def getVehicles():
	now = int(time.time() * 1000)
	twentySecondsAgo = now - (20 * 1000)
	lastRequestTime = 0
	with open('data/ttc_vehicles.json') as ttcVehicles:
		vehiclesJSON = json.load(ttcVehicles)
		lastRequestTime = int(vehiclesJSON['5']['lastRequestTime'])
	if lastRequestTime < twentySecondsAgo:
		vehicles = requestNextBusData('vehicleLocations', 'r='+'5'+'&t='+str(lastRequestTime))
		# vehicles = '<?xml version="1.0" encoding="utf-8" ?> \
	# <body copyright="All data copyright Toronto Transit Commission 2013.">\
	# <vehicle id="1377" routeTag="5" dirTag="5_0_5" lat="43.706066" lon="-79.400146" secsSinceReport="3" predictable="true" heading="348"/>\
	# <vehicle id="1383" routeTag="5" dirTag="5_0_5" lat="43.660568" lon="-79.390984" secsSinceReport="16" predictable="true" heading="83"/>\
	# <vehicle id="8312" routeTag="5" dirTag="5_1_5" lat="43.676666" lon="-79.397285" secsSinceReport="0" predictable="true" heading="344"/>\
	# <lastTime time="1360019007607"/>\
	# </body>'
		soup = BeautifulSoup(vehicles, 'xml')
		vehiclesJSON = {}
		vehicleList = []
		for vehicle in soup.find_all('vehicle'):
			vehicleList.append({ 'id' : vehicle['id'], 'dirTag' : vehicle['dirTag'], 'lat' : float(vehicle['lat']), 'lon' : float(vehicle['lon']), 'heading' : int(vehicle['heading']), 'reported' : int(vehicle['secsSinceReport']), 'predictable' : vehicle['predictable']})
		vehiclesJSON.update({ '5' : {'lastRequestTime': soup.lastTime['time'], 'vehicles': vehicleList}})
		open('data/ttc_vehicles.json', 'w').write(json.dumps(vehiclesJSON, indent=2))
	return json.dumps(vehiclesJSON, indent=2)

def getAlerts():
	index_html = requests.get('http://ttc.ca/Service_Advisories/all_service_alerts.jsp')
	soup = BeautifulSoup(index_html.text)
	advisory_wrap = soup.find(class_="advisory-wrap")
	alerts = []
	for alert_content in advisory_wrap.find_all('div'):
		alerts.append((alert_content.find(class_="veh-replace").string, alert_content.find(class_="alert-updated").string[13:]))
	return alerts

if __name__=="__main__":
	# print getPredictions(43.7739, -79.41427)
	# print getRoutes()
	# open('data/ttc_routes.json', 'w').write(getRoutes())
	# print getStops()
	# open('data/ttc_stops.json', 'w').write(getStops())
	getVehicles()
	# print getAlerts()
