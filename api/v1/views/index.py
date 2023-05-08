#!/usr/bin/python3
"""Create root using registered blueprint"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """Return json of status"""

    return jsonify({"status": "OK"})
