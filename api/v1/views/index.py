#!/usr/bin/python3
"""Create root using registered blueprint"""

from api.v1.views import app_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """Return json of status"""

    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """Return the number of objects present in the database"""

    stats = {}
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}

    for key, value in classes.items():
        count_obj = models.storage.count(value)
        stats[key] = count_obj

    return jsonify(stats)
