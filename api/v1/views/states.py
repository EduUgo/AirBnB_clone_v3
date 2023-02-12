#!/usr/bin/python3
"""State view"""

from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed
from api.v1.views import app_views
from models import storage
from models.state import State

methods_allowed = ['GET', 'DELETE', 'POST', 'PUT']


@app_views.route('/states', methods=methods_allowed)
@app_views.route('/states/<id>', methods=methods_allowed)
def state_handler(id=None):
    """Handle function for State endpoints."""
    handlers = {
        'GET': get_states,
        'POST': create_state,
        'DELETE': delete_state,
        'PUT': update_state
        }
    if request.method in methods_allowed:
        return handlers[request.method](id)
    else:
        raise MethodNotAllowed(methods_allowed)


def get_states(id):
    """Retrieves all State objects or a state by ID."""
    states = storage.all(State)
    if id:
        state = storage.get(State, id)
        if state:
            return state.to_dict()
        raise NotFound
    states_list = list(map(lambda x: x.to_dict(), states.values()))
    return jsonify(states_list)


def create_state(id):
    """Creates a new State object."""
    try:
        data = request.get_json()
    except Exception:
        raise BadRequest(description='Not a JSON')

    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


def delete_state(id):
    """Deletes a State object by id."""
    state = storage.get(State, id)
    if state:
        state.delete()
        storage.save()
        return {}, 200
    raise NotFound


def update_state(id):
    """Updates a State object by id."""
    state = storage.get(State, id)
    if not state:
        raise NotFound
    try:
        data = request.get_json()
    except Exception:
        raise BadRequest(description='Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
