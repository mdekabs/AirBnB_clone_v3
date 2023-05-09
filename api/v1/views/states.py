#!/usr/bin/python3
"""Script to render the states data"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def states(state_id=None):
    """Get all the states data"""
    states_obj = storage.all(State)
    """'{{State.__class__.__name__}.{Object.id}': row_obj} is
    returned for each State value"""

    if not state_id:
        if request.method == 'GET':
            states_list = [value.to_dict() for value in states_obj.values()]
            return jsonify(states_list)

        if request.method == 'POST':
            """Get the json data from the request body"""
            data_json = request.get_json()

            """Check if the data is not json"""
            if not data_json:
                abort(400, 'Not a JSON')
            """Check if data doesn't contain name"""
            if data_json.get('name') is None:
                abort(400, 'Missing name')

            """Create and save the new object"""
            new = State(**data_json)
            new.save()
            return jsonify(new.to_dict()), 201

    else:
        if request.method == 'GET':
            search = "{}.{}".format(State.__name__, state_id)
            if search in states_obj:
                return jsonify(states_obj[search].to_dict())
            abort(404)

        if request.method == 'DELETE':
            search = "{}.{}".format(State.__name__, state_id)
            if search in states_obj:
                storage.delete(states_obj[search])
                storage.save()
                return jsonify({}), 200
            abort(404)

        if request.method == 'PUT':
            """Get the json data from the request body"""
            data_json = request.get_json()

            """Check if the data is not json"""
            if not data_json:
                abort(400, 'Not a JSON')
            """Check if data doesn't contain name"""
            search = "{}.{}".format(State.__name__, state_id)
            if search in states_obj:
                """Update the obj with the new value"""
                states_obj[search].name = data_json.get('name')
                states_obj[search].save()
                return jsonify(states_obj[search].to_dict())
            abort(404)
