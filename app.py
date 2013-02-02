#!/usr/bin/env python
import os
import json
from flask import Flask, request, render_template, Response, url_for, jsonify, send_from_directory
from werkzeug import SharedDataMiddleware
from ttc_request import getPredictions

app = Flask(__name__, template_folder='public')
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), 'public')
})

@app.route('/')
def root():
    return send_from_directory('public', 'index.html')

@app.route('/get', methods = ['GET']) 
def getStops():
    lat = request.args["lat"] 
    lon = request.args["lon"]
    resp = createResponse(lat,lon)
    return jsonify(resp)

def createResponse(lat,lon):
    upcoming = getPredictions(float(lat), float(lon))
    upcoming = json.loads(upcoming)
    stops = []
    for stop in upcoming["Predictions"]:
        if stop:
            route = createRoute(stop[1], stop[4], stop[6], stop[5])
            stop = createStop(stop[2], stop[3], [route])
            stops.append(stop)
    responseJSON = {"stops" : stops}
    return responseJSON

def createStop(lat, lon, routes):
    return {'lat':lat,'lon':lon, 'routes':routes}

def createRoute(routeType, name, times, direction):
    return {'type':routeType, 'name':name, 'times':times, 'direction':direction}
 
def createTimes(times):
    return times

if __name__ == '__main__':
    print createResponse("43.7196699","-79.4012199")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
