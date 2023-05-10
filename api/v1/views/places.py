#!/usr/bin/python3

"""Script that handles all RESTFUL API Functions for Place Object"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places__by_city(city_id):
    """retrieve places based on city_id"""
    city_objs = storage.all(City)
    """'{{City.__class__.__name__}.{City.id}': row_obj} is
    returned for each city value"""
    cities = [obj for obj in city_objs.values()]

    if request.method == 'GET':
        for city in cities:
            if city.id == city_id:
                places_objs = storage.all(Place)
                places = [obj.to_dict() for obj in
                          places_objs.values() if obj.city_id == city_id]
                return jsonify(places)
        abort(404)

    if request.method == 'POST':
        for city in cities:
            if city.id == city_id:
                my_dict = request.get_json()
                if my_dict is None:
                    abort(400, 'Not a JSON')

                user_id = my_dict.get("user_id")
                if not user_id:
                    abort(400, 'Missing user_id')
                if user_id:
                    user_objs = storage.all(User)
                    user = [True for obj in user_objs.values()
                            if obj.id == user_id]
                    if not user:
                        abort(404)

                if my_dict.get("name") is None:
                    abort(400, 'Missing name')

                my_dict["city_id"] = city_id
                my_dict["user_id"] = user_id
                place = Place(**my_dict)
                place.save()
                return jsonify(place.to_dict()), 201
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def place_by_place_id(place_id):
    """retrieves place by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        for k, v in my_dict.items():
            setattr(place, k, v)
        place.save()
        return jsonify(place.to_dict()), 200
