#!/usr/bin/python3
"""Start a flask app and register a Blueprint"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(exception):
    """End the session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Handles the 404 error page"""

    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'
    app.run(host=host, port=int(port), threaded=True)
