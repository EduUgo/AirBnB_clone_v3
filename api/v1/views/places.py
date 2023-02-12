#!/usr/bin/python3

from api.v1.views import app_views
from models import storage, storage_t
from flask import request, jsonify
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from werkzeug.exceptions import NotFound, BadRequest


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Retrieves all the Place objects of a City."""
    city = storage.get(City, city_id)
    if city:
        return jsonify(list(map(lambda x: x.to_dict(), city.places)))
    raise NotFound


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object by its ID."""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    raise NotFound


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object."""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        storage.save()
        return {}, 200
    raise NotFound


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a new Place object."""
    city = storage.get(City, city_id)
    if city:
        try:
            data = request.get_json()
        except Exception:
            raise BadRequest("Not a JSON")

        if 'user_id' not in data:
            raise BadRequest("Missing user_id")
        if storage.get(User, data['user_id']) is None:
            raise NotFound
        if 'name' not in data:
            raise BadRequest("Missing name")

        new_place = Place(city_id=city_id, **data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    raise NotFound


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place:
        try:
            data = request.get_json()
        except Exception:
            raise BadRequest("Not a JSON")

        for key, value in data.items():
            if key not in [
                'id',
                'user_id',
                'city_id',
                'created_at',
                'updated_at'
            ]:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    raise NotFound


@app_views.route('/places_search', methods=['GET'])
def places_search():
    """Gets places objects"""
    try:
        data = request.get_json()
    except Exception:
        raise BadRequest("Not a JSON")

    if data:
        cities = []
        places = []
        filterd = []
        if 'states' in data:
            for state_id in data['states']:
                state = storage.get(State, state_id)
                if state:
                    cities.extend(state.cities)

        if 'cities' in data:
            for city_id in data['cities']:
                city = storage.get(City, city_id)
                if city and city not in cities:
                    cities.append(city)

        for city_ in cities:
            places.extend(city_.places)

        if 'amenities' in data:
            for amenity_id in data['amenities']:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    for place in places:
                        if storage_t == 'db':
                            if amenity in place.amenities:
                                delattr(place, 'amenities')
                                filterd.append(place)
                        else:
                            if amenity in place.amenities():
                                delattr(place, 'amenities')
                                filterd.append(place)

            return (list(map(lambda x: x.to_dict(), filterd)))

        return list(map(lambda x: x.to_dict(), places))
    else:
        places = storage.all(Place)
        return jsonify(list(map(lambda x: x.to_dict(), places.values())))
