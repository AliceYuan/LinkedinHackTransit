#!/usr/bin/env python

import json, requests
import xml.etree.ElementTree as ET

stops = []

def requestNextBusData(commandName, params):
	base_url = 'http://webservices.nextbus.com/service/publicXMLFeed'
	agencyTag = 'ttc'
	request_url = base_url + '?' + 'command=' + commandName + '&' + 'a=' + agencyTag + '&' + params
	result = requests.get(request_url).text
	return result

if __name__=="__main__":
	routes = requestNextBusData('routeList', 'r=')
	rootRoutelist = ET.fromstring(routes)
	for route in rootRoutelist:
		currentRoute = requestNextBusData('routeConfig', 'r='+route.attrib['tag'])
		rootCurrentRoute = ET.fromstring(currentRoute)
		for route in rootCurrentRoute.findall('route'):
			for stop in route.findall('stop'):
				stops.append(stop.attrib)

	data = { "Stops" : stops }
	with open('ttc_stops.json', 'a') as ttcStops:
		ttcStops.write(json.dumps(data, indent=2))
