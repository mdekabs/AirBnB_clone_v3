#!/usr/bin/python3
"""Create root using registered blueprint"""

from api.v1.views import app_views
import jsonify

@app_views.route('/status')
def status():
    """Return json of staus"""
    return jsonify({"status": "OK"})