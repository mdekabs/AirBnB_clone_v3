#!/usr/bin/python3

"""Script that handles all RESTFUL API Functions for Place Object"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
# Note: Adding endpoint to the route (endpoint='anyname') will
# prevent AssertionError during deployment using WSGI
# (function mapping overwriting).
def reviews__by_place(place_id):
    """retrieve places based on city_id"""
    place_objs = storage.all(Place)
    """'{{Place.__class__.__name__}.{Place.id}': row_obj} is
    returned for each place value"""
    places = [obj for obj in place_objs.values()]

    if request.method == 'GET':
        for place in places:
            if place.id == place_id:
                reviews_objs = storage.all(Review)
                reviews = [obj.to_dict() for obj in
                           reviews_objs.values() if obj.place_id == place_id]
                return jsonify(reviews)
        abort(404)

    if request.method == 'POST':
        for place in places:
            if place.id == place_id:
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

                if my_dict.get("text") is None:
                    abort(400, 'Missing text')

                my_dict["place_id"] = place_id
                my_dict["user_id"] = user_id
                review = Review(**my_dict)
                review.save()
                return jsonify(review.to_dict()), 201
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def review_by_review_id(review_id):
    """retrieves place by place_id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        my_dict = request.get_json()
        if my_dict is None:
            abort(400, 'Not a JSON')
        for k, v in my_dict.items():
            setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict()), 200
