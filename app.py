#!/usr/bin/env python
import os
import collections
import json
from flask import Flask, request, render_template, Response, url_for, jsonify, send_from_directory
from werkzeug import SharedDataMiddleware
from ttc_request import getPredictions
from time import time

cache = None
last_cached = 0

app = Flask(__name__, template_folder='public')
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), 'public')
})

@app.route('/')
def root():
    return send_from_directory('public', 'index.html')

@app.route('/get', methods = ['GET']) 
def getStops():
    global cache
    global last_cached
    lat = request.args["lat"] 
    lon = request.args["lon"]
    if cache is None or time() - last_cached > 5*60:
        cache = createResponse(lat,lon)
        last_cached = time()
    return jsonify(cache)

def createResponse(lat,lon):
    upcoming = getPredictions(float(lat), float(lon))
    upcoming = json.loads(upcoming)
    stops = collections.OrderedDict()
    for stop in upcoming["Predictions"]:
        if stop:
            route = createRoute(stop[1], stop[6], stop[5])
            stopend = createStop(stop[2], stop[3], stop[4], [route])
            if str(stop[2])+str(stop[3]) not in stops:
                stops[str(stop[2])+str(stop[3])] = stopend
            else:
                val = stops[str(stop[2]) + str(stop[3])]
                val['routes'].append(route)
                stops[str(stop[2])+str(stop[3])] = val
    resp = []
    for k,v in stops.items():
        resp.append(v)
    responseJSON = {"stops" : resp}
    return responseJSON

def createStop(lat, lon, intersection, routes):
    return {'lat':lat,'lon':lon, 'name':intersection, 'routes':routes}

def createRoute(routeTag, times, direction):
    return {'type':routeTag, 'times':times, 'direction':direction}
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
