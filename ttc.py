#!/usr/bin/env python

import json, math, requests, time, collections
from bs4 import BeautifulSoup

def getNextBusData(params):
	payload = {}
	for paramName, param in params.iteritems():
		payload.update({paramName: param})
	payload.update({'a': 'ttc'})
	r = requests.get('http://webservices.nextbus.com/service/publicXMLFeed', params=payload)
	return r.text

def getRoutes():
	routes = getNextBusData({'command': 'routeList'})
	soup = BeautifulSoup(routes, 'xml')
	rootRoutelist = soup.body.find_all('route')
	routeList = []
	for route in rootRoutelist:
		routeList.append({'routeTag': route['tag'], 'routeTitle': route['title']})
	routeJSON = { 'routes' : routeList }
	return json.dumps(routeJSON, indent=4)

def getStops():
	with open('data/ttc_routes.json') as ttcRoutes:
		routeList = json.load(ttcRoutes)['routes']
	stopList = []
	for route in routeList:
		currentRoute = getNextBusData({'command': 'routeConfig', 'r': route['routeTag'], 'terse': ''})
		soup = BeautifulSoup(currentRoute, 'xml')
		rootCurrentRoute = soup.route.find_all('stop', recursive=False)
		for stop in rootCurrentRoute:
			stopList.append({'routeTag': soup.route['tag'], 'routeTitle': soup.route['title'], 'stopTag': stop['tag'], 'lat': float(stop['lat']), 'lon': float(stop['lon'])})
	stopJSON = { 'stops' : stopList }
	return json.dumps(stopJSON, indent=4)

def getNearbyStops(latitude, longitude):
	stops = []
	distances = []
	with open('data/ttc_stops.json') as ttcStops:
		stops = json.load(ttcStops)['stops']
	for stop in stops:
		d = distance([latitude, longitude], [float(stop['lat']), float(stop['lon'])])
		stop.update({'distance': d})
		distances.append(d)
	stops = [stops for (distances, stops) in sorted(zip(distances, stops))]
	stopsJSON = { 'stops' : stops }
	return json.dumps(stopsJSON, indent=4)

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

def getPredictions(latitude, longitude):
	predictionList = []
	nearbyStops = json.loads(getNearbyStops(latitude, longitude))['stops']
	nearbyStops = filterNearbyStops(nearbyStops)
	for stop in nearbyStops:
		predictions = getNextBusData({'command': 'predictions', 'r': stop['routeTag'], 's': stop['stopTag']})
		soup = BeautifulSoup(predictions, 'xml')
		predictions = soup.predictions
		if predictions.has_attr('dirTitleBecauseNoPredictions'):
			predictionList.append({'routeTag': predictions['routeTag'], 'routeTitle': predictions['routeTitle'], 'stopTag': predictions['stopTag'], 'stopTitle': predictions['stopTitle'], 'distance': stop['distance'], 'minutes': ['-']})
		else:
			dList = []
			for direction in predictions.find_all('direction'):
				pList = []
				mList = []
				for prediction in direction.find_all('prediction'):
					pList.append({'branch': prediction['branch'], 'dirTag': prediction['dirTag'], 'vehicle': prediction['vehicle'], 'minutes': prediction['minutes'], 'epochTime': prediction['epochTime']})
					mList.append(prediction['minutes'])
				dList.append({direction['title']: pList})
			predictionList.append({'routeTag': predictions['routeTag'], 'routeTitle': predictions['routeTitle'], 'stopTag': predictions['stopTag'], 'stopTitle': predictions['stopTitle'], 'distance': stop['distance'], 'directions': dList, 'minutes': mList})
	predictionJSON = { 'predictions' : predictionList }
	return json.dumps(predictionJSON, indent=4)

def filterNearbyStops(stops):
	uniqueStops = collections.OrderedDict()
	uniqueStopList = []
	for stop in stops:
		if stop['routeTag'] not in uniqueStops:
			uniqueStops.update({stop['routeTag']: stop})
	for uniqueStop in uniqueStops.values():
		uniqueStopList.append(uniqueStop)
	uniqueStopList = uniqueStopList[:5]
	return uniqueStopList

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
	r = requests.get('http://ttc.ca/Service_Advisories/all_service_alerts.jsp')
	soup = BeautifulSoup(r.text)
	advisory_wrap = soup.find(class_="advisory-wrap")
	alerts = []
	for alert_content in advisory_wrap.find_all('div'):
		alerts.append((alert_content.find(class_="veh-replace").string, alert_content.find(class_="alert-updated").string[13:]))
	return alerts

if __name__=="__main__":
	# print getRoutes()
	# open('data/ttc_routes.json', 'w').write(getRoutes())
	# print getStops()
	# open('data/ttc_stops.json', 'w').write(getStops())
	# print getNearbyStops(43.7739, -79.41427)
	print getPredictions(43.7739, -79.41427)
	# getVehicles()
	# print getAlerts()
