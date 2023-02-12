#!/usr/bin/python3


from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """Retrieves all Review objects for a given Place object."""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(list(map(lambda x: x.to_dict(), place.reviews)))
    raise NotFound


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieves a Review object by ID."""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    raise NotFound


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object."""
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return {}, 200
    raise NotFound


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a Review object."""
    place = storage.get(Place, place_id)
    if place:
        try:
            data = request.get_json()
            data['place_id'] = place_id
        except Exception:
            raise BadRequest("Not a JSON")

        if 'user_id' not in data:
            raise BadRequest("Missing user_id")
        if storage.get(User, data['user_id']) is None:
            raise NotFound
        if 'text' not in data:
            raise BadRequest("Missing text")

        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    raise NotFound


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object."""
    review = storage.get(Review, review_id)
    if review:
        try:
            data = request.get_json()
        except Exception:
            raise BadRequest("Not a JSON")

        for key, value in data.items():
            if key not in [
                'id',
                'user_id',
                'place_id',
                'created_at',
                'updated_at'
            ]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    raise NotFound
