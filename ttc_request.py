#!/usr/bin/env python

import requests

base_url = 'http://webservices.nextbus.com/service/publicXMLFeed'

commandName = 'routeConfig'
agencyTag = 'ttc'
route = '501'

def getRoutes():
	request_url = base_url + '?' + 'command=' + commandName + '&' + 'a=' + agencyTag + '&' + 'r=' + route
	result = requests.get(request_url).text
	return result

routes = getRoutes()
print routes
