#!/usr/bin/python3

"""Script to render the cities data"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

"""Get all the cities obj from the storage
'{{State.__class__.__name__}.{Object.id}': row_obj} is
    returned for each State value"""
cities_obj = storage.all(City)


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def state_cities(state_id):
    """HTTP methods with all the cities data"""

    """Get the state with state_id given"""
    state = [True for obj in storage.all(State).values()
              if obj.id == state_id]
    """Get all the cities with specific state_id"""
    cities = [obj.to_dict() for obj in cities_obj.values()
              if obj.state_id == state_id]

    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify(cities)

    if request.method == 'POST':
        """Create a new city data
        Get the json data from the request body"""
        data_json = request.get_json()

        """Check if the state_id is valid before creating a new city
        for the State. If it is valid, there will be cities with the
        state_id else abort with 404."""
        if cities:
            """Check if the data is not json"""
            if not data_json:
                abort(400, 'Not a JSON')
            """Check if data doesn't contain name"""
            if data_json.get('name') is None:
                abort(400, 'Missing name')

            """Add the state_id into the data_json"""
            data_json['state_id'] = state_id
            """Create and save the new object"""
            new = City(**data_json)
            new.save()
            return jsonify(new.to_dict()), 201
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def city(city_id):
    """HTTP methods with all cities data"""

    if not city_id:
        abort(404)

    else:
        """Get a specific city with city_id"""
        city = storage.get(City, city_id)

        if city:
            if request.method == 'GET':
                return jsonify(city.to_dict())

            if request.method == 'DELETE':
                storage.delete(city)
                storage.save()
                return jsonify({}), 200

            if request.method == 'PUT':
                """Get the json data from the request body"""
                data_json = request.get_json()

                """Check if the data is not json"""
                if not data_json:
                    abort(400, 'Not a JSON')

                """Update the obj with the new value"""
                city.name = data_json.get('name')
                city.save()
                return jsonify(city.to_dict()), 200

        abort(404)
