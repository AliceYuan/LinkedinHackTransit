#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

def getAlerts():
	index_html = requests.get('http://ttc.ca/Service_Advisories/all_service_alerts.jsp')
	soup = BeautifulSoup(index_html.text)
	advisory_wrap = soup.find(class_="advisory-wrap")
	alerts = []
	for alert_content in advisory_wrap.find_all('div'):
		alerts.append((alert_content.find(class_="veh-replace").string, alert_content.find(class_="alert-updated").string[13:]))
	return alerts

if __name__=="__main__":
	print getAlerts()
