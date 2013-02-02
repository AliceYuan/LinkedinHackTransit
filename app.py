import os
from flask import Flask, request, render_template, Response, url_for
from werkzeug import SharedDataMiddleware

app = Flask(__name__, template_folder='public')
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
  '/public': os.path.join(os.path.dirname(__file__), 'public')
})

@app.route('/')
def root():
    return render_template('test.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
