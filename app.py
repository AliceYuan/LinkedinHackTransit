#!/usr/bin/env python
import os
import json
from flask import Flask, request, render_template, Response, url_for, jsonify, send_from_directory
from werkzeug import SharedDataMiddleware

app = Flask(__name__, template_folder='public')
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), 'public')
})

@app.route('/')
def root():
    return send_from_directory('public', 'app.html')

@app.route('/get', methods = ['GET']) 
def getStops():
    return send_from_directory('public', 'data.json')
#    lat = request.args["lat"] 
#   lon = request.args["lon"]
#   lat = "43.7196699"
#   lon = "-79.4012199"
#   resp = createResponse(lat,lon)
#   return jsonify(resp)

#def createResponse(lat,lon):
#    upcoming = ttc_times.getUpcomingDepartures(float(lat),float(lon))
##    upcoming = ""
#  stops = []
#   for stop in upcoming["Departures"]:
#       if stop:
#           route = createRoute("TTC", stop["route"], stop["minutes"])
#           stop = createStop(stop["lat"], stop["lon"], [route])
#           stops.append(stop)
#   responseJSON = {"stops" : stops}
#   return responseJSON

def createStop(lat, lon, routes):
    return {'lat':lat,'lon':lon, 'routes':routes}

def createRoute(routeType, name, times):
    return {'type':routeType, 'name':name, 'times':times}
 
def createTimes(times):
    return times

if __name__ == '__main__':
#print createResponse("43.7196699","-79.4012199")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
