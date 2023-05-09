#!/usr/bin/python3
"""Script to render the cities data"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models import storage

"""Get all the cities obj from the storage"""
cities_obj = storage.all(City)


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'], strict_slashes=False)
# @app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def state_cities(state_id):
    """Get the cities of a given state"""
    if not state_id:
        abort(404)
