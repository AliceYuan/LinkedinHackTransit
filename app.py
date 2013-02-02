import os
from flask import Flask, request, render_template, Response, url_for, jsonify, send_from_directory
from werkzeug import SharedDataMiddleware

app = Flask(__name__, template_folder='public')
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/': os.path.join(os.path.dirname(__file__), 'public')
})

@app.route('/')
def root():
    return send_from_directory('public', 'test.html')

@app.route('/getStops', methods = ['GET']) 
def getStops():
    routes = [
       {'lat': 1, 
        'lon': 2, 
        'type':""
       }
    ]
    return jsonify(results = routes)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
