#!/usr/bin/env python
import os, json, collections
from flask import Flask, request, render_template, Response, url_for, jsonify, send_from_directory
from werkzeug import SharedDataMiddleware
import ttc

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
	return jsonify(createResponse(lat,lon))

def createResponse(lat,lon):
	predictions = json.loads(ttc.getPredictions(float(lat), float(lon)))
	# uniqueStops = collections.OrderedDict()
	stops = []
	for stop in predictions['predictions']:
		dList = []
		for direction in stop['directions']:
			directionDict = {}
			for dirName,details in direction.iteritems():
				mList = []
				for prediction in details:
					mList.append(prediction['minutes'])
			directionDict.update({'direction': dirName, 'type': stop['routeTag'], 'times': mList})
		dList.append(directionDict)
		stops.append({'name': stop['stopTitle'], 'lat': stop['lat'], 'lon': stop['lon'], 'routes': dList})
		# route = createRoute(stop['routeTag'], [0], stop['routeTitle'])
		# stopend = createStop(stop['lat'], stop['lon'], stop['stopTitle'], dList)
		# if str(stop['lat'])+str(stop['lon']) not in uniqueStops:
		# 	uniqueStops.update({str(stop['lat'])+str(stop['lon']): stopend})
		# else:
		# 	val = uniqueStops[str(stop['lat']) + str(stop['lon'])]
		# 	val['routes'].append(route)
		# 	uniqueStops.update({str(stop['lat'])+str(stop['lon']): val})
	# resp = []
	# for k,v in uniqueStops.items():
	# 	resp.append(v)
	responseJSON = { 'stops' : stops }
	return responseJSON

def createStop(lat, lon, intersection, routes):
	return {'lat':lat,'lon':lon, 'name':intersection, 'routes':routes}

def createRoute(routeTag, times, direction):
	return {'type':routeTag, 'times':times, 'direction':direction}

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
	# print json.dumps(createResponse(43.7739, -79.41427), indent=4)
