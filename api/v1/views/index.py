#!/usr/bin/python3
"""Create root using registered blueprint"""

from api.v1.views import app_views
import json

@app_views.route('/status')
def status():
    """Return json of staus"""
    stat_json = json.dumps({"status": "OK"})
    return stat_json