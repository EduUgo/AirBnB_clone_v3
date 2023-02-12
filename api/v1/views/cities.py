#!usr/bin/python3
"""Cities views."""

from api.v1.views import app_views
from flask import request, jsonify
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest
from models.city import City
from models.state import State
from models import storage

methods_allowed = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/cities', methods=methods_allowed)
@app_views.route('/cities/<city_id>', methods=methods_allowed)
@app_views.route('/states/<state_id>/cities', methods=methods_allowed)
def city_handler(state_id=None, city_id=None):
    """Handle function for City endpoints."""
    handlers = {
        'GET': get_cities,
        'POST': create_city,
        'DELETE': delete_city,
        'PUT': update_city
        }
    if request.method in methods_allowed:
        return handlers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(methods_allowed)


def get_cities(state_id=None, city_id=None):
    """Rrtrieves all City objects of a State or one City object by ID"""
    if state_id:
        state = storage.get(State, state_id)
        if state:
            cities = list(map(lambda x: x.to_dict(), state.cities))
            return jsonify(cities)
        raise NotFound

    if city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
        raise NotFound

    return jsonify(list(map(lambda x: x.to_dict(),
                   storage.all(City).values())))


def create_city(state_id, city_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state:
        try:
            data = request.get_json()
        except Exception:
            raise BadRequest("Not a JSON")

        if "name" not in data:
            raise BadRequest("Missing name")
        if "state_id" not in data:
            raise BadRequest("Missing state_id")

        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    raise NotFound


def delete_city(state_id, city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        city.delete()
        storage.save()
        return {}, 200
    raise NotFound


def update_city(state_id, city_id):
    """Updates a City object."""
    city = storage.get(City, city_id)
    if city:
        try:
            data = request.get_json()
        except Exception:
            raise BadRequest("Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    raise NotFound
