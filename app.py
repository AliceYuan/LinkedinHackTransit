#!/usr/bin/env python
import os
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
    #lat = request.args["lat"] 
    #lon = request.args["lon"]
    #resp = createResponse(lat,lon)
    #return jsonify(resp)
    return send_from_directory('public', 'data.json')

def createResponse(lat,lon):
    times = createTimes([100,2900,3000])
    routeType = "TTC"
    name = "route"
    routes = [createRoute(routeType, name, times)]
    stop = createStop(lat,lon, routes)
    responseJSON = {"routes": [stop, stop, stop]}
    return responseJSON

def createStop(lat, lon, routes):
    return {'lat':lat,'lon':lon, 'routes':routes}

def createRoute(routeType, name, times):
    return {'type':routeType, 'name':name, 'times':times}
 
def createTimes(times):
    return times

if __name__ == '__main__':
    print createResponse("10","10")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
