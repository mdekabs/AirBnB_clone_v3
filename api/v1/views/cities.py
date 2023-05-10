#!/usr/bin/python3
"""Script to render the cities data"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models import storage

"""Get all the cities obj from the storage"""
cities_obj = storage.all(City)


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def state_cities(state_id):
    """HTTP methods with all the cities data"""
    if not state_id:
        abort(404)

    """Get all the cities with specific state_id"""
    cities = [value.to_dict() for value in cities_obj.values()
              if value.state_id == state_id]

    if request.method == 'GET':
        if cities:
            return jsonify(cities)
        abort(404)

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

    if request.method == 'GET':
        """Get a specific city with city_id"""
        search = "{}.{}".format(City.__name__, city_id)
        if search in cities_obj:
            return jsonify(cities_obj[search].to_dict())
        abort(404)

    if request.method == 'DELETE':
        """Delete the city with the provided city_id"""
        search = "{}.{}".format(City.__name__, city_id)
        if search in cities_obj:
            storage.delete(cities_obj[search])
            storage.save()
            return jsonify({})
        abort(404)

    if request.method == 'PUT':
        """Get the json data from the request body"""
        data_json = request.get_json()

        """Check if the data is not json"""
        if not data_json:
            abort(400, 'Not a JSON')

        search = "{}.{}".format(City.__name__, city_id)
        if search in cities_obj:
            """Update the obj with the new value"""
            cities_obj[search].name = data_json.get('name')
            cities_obj[search].save()
            return jsonify(cities_obj[search].to_dict())
        abort(404)