#!/usr/bin/python3
"""Amenity view"""

from flask import jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Retrieves all Amenity objects."""
    amenities = storage.all(Amenity)
    return jsonify(list(map(lambda x: x.to_dict(), amenities.values())))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    raise NotFound


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Retrieves an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        amenity.delete()
        storage.save()
        return {}, 200
    raise NotFound


@app_views.route('amenities', methods=['POST'])
def create_amenity():
    """Creates a new Amenity."""
    try:
        data = request.get_json()
    except Exception:
        raise BadRequest("Not a JSON")

    if 'name' not in data:
        raise BadRequest("Missing name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        try:
            data = request.get_json()
        except Exception:
            raise BadRequest("Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'create_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    raise NotFound
