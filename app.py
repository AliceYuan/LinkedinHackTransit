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
    lat = []
    lon = []
    for stop in upcoming["Predictions"]:
        if stop:
            route = createRoute(stop[1], stop[6], stop[5])
            stop = createStop(stop[2], stop[3], stop[4], [route])
            stops.append(stop)
    responseJSON = {"stops" : stops}
    return responseJSON

def createStop(lat, lon, intersection, routes):
    return {'lat':lat,'lon':lon, 'intersection':intersection, 'routes':routes}

def createRoute(routeTag, times, direction):
    return {'type':routeTag, 'times':times, 'direction':direction}
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
