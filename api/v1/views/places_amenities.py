#!/usr/bin/python3
"""Place-Amenity views."""

from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, request
from werkzeug.exceptions import NotFound


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities(place_id):
    """Retrieves the Amenity objects tied to a Place object."""
    place = storage.get(Place, place_id)
    if place:
        if storage_t:
            return jsonify(list(map(lambda x: x.to_dict(), place.amenities)))
        else:
            return jsonify(list(map(lambda x: x.to_dict(), place.amenities())))
    raise NotFound


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'])
def link_place_amenity(place_id, amenity_id):
    """Links/Deletes a Place-Amenity object pair."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place and amenity:
        if storage_t:
            place_amenity = amenity if amenity in place.amenities else None
        else:
            place_amenity = amenity if amenity in place.amenities() else None

        if request.method == 'POST':
            if place_amenity:
                return jsonify(place_amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
                storage.save()
                return jsonify(amenity.to_dict()), 201

        if request.method == 'DELETE':
            if place_amenity:
                place.amenities.remove(place_amenity)
                storage.save()
                return {}, 200

    raise NotFound
