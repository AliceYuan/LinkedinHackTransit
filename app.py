#!/usr/bin/env python
import os, json, collections
from flask import Flask, request, render_template, Response, url_for, jsonify, send_from_directory
from werkzeug import SharedDataMiddleware
import ttc

cache = None

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
    lat = request.args["lat"] 
    lon = request.args["lon"]
    if cache is None:
        cache = createResponse(lat,lon)
    return jsonify(cache)

@app.route('/update')
def update():
    global cache
    cache = None
    return "updated cache"

def createResponse(lat,lon):
    upcoming = ttc.getPredictions(float(lat), float(lon))
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
