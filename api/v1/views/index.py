#!/usr/bin/python3
"""Index module for api views"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Returns a Status: OK Json."""
    return jsonify(status='OK')


@app_views.route('stats')
def count():
    """Returns the count of each object type"""
    classes = {
        'amenities': 'Amenity',
        'cities': 'City',
        'places': 'Place',
        'reviews': 'Review',
        'states': 'State',
        'users': 'User'
        }
    for class_ in classes.keys():
        classes[class_] = storage.count(classes.get(class_))
    return jsonify(classes)
