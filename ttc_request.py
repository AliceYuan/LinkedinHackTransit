#!/usr/bin/env python

import json, requests
import xml.etree.ElementTree as ET

base_url = 'http://webservices.nextbus.com/service/publicXMLFeed'
agencyTag = 'ttc'

def requestNextBusData(commandName, routeTag):
	request_url = base_url + '?' + 'command=' + commandName + '&' + 'a=' + agencyTag + '&' + 'r=' + routeTag
	result = requests.get(request_url).text
	return result

routes = requestNextBusData('routeList', '')
rootRoutelist = ET.fromstring(routes)
for route in rootRoutelist:
	currentRoute = requestNextBusData('routeConfig', route.attrib['tag'])
	rootCurrentRoute = ET.fromstring(currentRoute)
	for route in rootCurrentRoute.findall('route'):
		for stop in route.findall('stop'):
			with open('ttc_stops.json', 'a') as ttcStops:
				ttcStops.write(json.dumps(stop.attrib) + "\n")
