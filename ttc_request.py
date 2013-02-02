#!/usr/bin/env python

import requests

request = 'http://webservices.nextbus.com/service/publicXMLFeed'

commandName = 'routeConfig'
agencyTag = 'ttc'
route = '501'

def getSchedule():
	url = request + '?' + 'command=' + '&' + 'a=' + agencyTag + '&' + 'r=' + route
	result = requests.get(url)
	return result

schedule = getSchedule()
print schedule
