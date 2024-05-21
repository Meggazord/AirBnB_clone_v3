#!/usr/bin/python3
"""
index file
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns Status OK """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ Returns Stats """

    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    counts = {value: storage.count(key) for key, value in classes.items()}
    return jsonify(counts)
