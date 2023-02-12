#!/usr/bin/python3
"""flask app"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins=['0.0.0.0'])


@app.teardown_appcontext
def teardown(exceptipon):
    """Tear down method."""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''Handles the 404 HTTP error code.'''
    return jsonify(error='Not found'), 404


@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code.'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400

# @app.errorhandler(405)
# def error_405(error):
#     return jsonify(error=error.valid_methods), 405


if __name__ == '__main__':
    H = getenv('HBNB_API_HOST')
    P = getenv('HBNB_API_PORT')
    Host = H if H else '0.0.0.0'
    Port = P if P else 5000
    app.run(host=Host, port=Port, threaded=True)
