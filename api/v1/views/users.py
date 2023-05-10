#!/usr/bin/python3

"""Script that handles all RESTFUL API Functions for User Object"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def users(user_id=None):
    """Retrieves a list of user obj"""

    user_objs = storage.all(User)
    """'{{User.__class__.__name__}.{User.id}': row_obj} is
    returned for each user value"""

    users = [obj.to_dict() for obj in user_objs.values()]
    if not user_id:
        if request.method == 'GET':
            return jsonify(users)
        if request.method == 'POST':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            if my_dict.get("email") is None:
                abort(400, 'Missing email')
            if my_dict.get("password") is None:
                abort(400, 'Missing password')
            new_user = User(**my_dict)
            new_user.save()
            return jsonify(new_user.to_dict()), 201
    else:
        if request.method == 'GET':
            for user in users:
                if user.get('id') == user_id:
                    return jsonify(user)
            abort(404)
        if request.method == 'PUT':
            my_dict = request.get_json()

            if my_dict is None:
                abort(400, 'Not a JSON')
            for user in user_objs.values():
                if user.id == user_id:
                    for k, v in my_dict.items():
                        setattr(user, k, v)
                    user.save()
                    return jsonify(user.to_dict()), 200
            abort(404)

        if request.method == 'DELETE':
            for obj in user_objs.values():
                if obj.id == user_id:
                    storage.delete(obj)
                    storage.save()
                    return jsonify({}), 200
            abort(404)
