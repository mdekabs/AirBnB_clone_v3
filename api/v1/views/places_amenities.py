#!/usr/bin/python3

"""Script that handles all RESTFUL API Functions
for PlaceAmenity Relationship
Warning: This code is an attempt to solve the advanced task
therefore the code might not run, it requires update"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def reviews__by_place(place_id, amenity_id=None):
    """retrieve places based on city_id"""
    place_objs = storage.all(Place)
    """'{{Place.__class__.__name__}.{Place.id}': row_obj} is
    returned for each place value"""
    places = [obj for obj in place_objs.values()]

    if not amenity_id:
        if request.method == 'GET':
            for place in places:
                if place.id == place_id:
                    amen_objs = storage.all(Amenity)
                    amenities = [obj.to_dict() for obj in amen_objs.values()
                                 if obj.id in place.amenities['amenity_id']]
                    return jsonify(amenities)
            abort(404)

    else:
        """Get the place obj with the given place_id and
        the amenity obj with the given amenity_id"""
        place = filter(lambda x: x.id == place_id, places)
        place_found = list(place)[0]
        amen_objs = storage.all(Amenity)
        amenities = [obj for obj in amen_objs.values()]
        amenity = filter(lambda x: x.id == amenity_id, amenities)
        amenity_found = list(amenity)[0]

        if not place_found or not amenity_found:
            abort(404)

        if request.method == 'DELETE':
            """Amenity is not linked to the Place before the request"""
            if place_found.amenities['amenity_id'] != amenity_id:
                abort(404)
            storage.delete(amenity_found)
            storage.save()
            return jsonify({}), 200

        if request.method == 'POST':
            if place_found.amenities['amenity_id'] == amenity_id:
                return jsonify(amenity_found.to_dict()), 200
            place_found.amenities['amenity_id'] = amenity_id
            return jsonify(amenity_found.to_dict()), 200
