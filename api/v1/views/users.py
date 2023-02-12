#!/usr/bin/python3
"""Users view."""

from models.user import User
from models import storage
from flask import request, jsonify
from werkzeug.exceptions import NotFound, BadRequest
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """Retrieves all User objects."""
    users = storage.all(User)
    return jsonify(list(map(lambda x: x.to_dict(), users.values())))


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves one User object by ID."""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    raise NotFound


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object."""
    user = storage.get(User, user_id)
    if user:
        user.delete()
        storage.save()
        return {}, 200
    raise NotFound


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a new User object."""
    try:
        data = request.get_json()
    except Exception:
        raise BadRequest("Not a JSON")

    if 'email' not in data:
        raise BadRequest("Missing email")
    if 'password' not in data:
        raise BadRequest("Missing password")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object."""
    user = storage.get(User, user_id)
    if user:
        try:
            data = request.get_json()
        except Exception:
            raise BadRequest("Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                if key == 'password':
                    user.set_password(data['password'])
                else:
                    setattr(user, key, value)

        user.save()
        return jsonify(user.to_dict()), 200
    raise NotFound
