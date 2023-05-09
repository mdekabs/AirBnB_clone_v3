#!/usr/bin/python3
"""Start a flask app and register a Blueprint"""

from flask import Flask
from flask import jsonify
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """End the session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Handles the 404 error page"""

    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'
    app.run(host=host, port=port, threaded=True)
