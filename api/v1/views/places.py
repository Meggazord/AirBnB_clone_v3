#!/usr/bin/python3
"""
Places file
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
        
@app.route('/api/v1/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    if not request.is_json:
        abort(400, description="Not a JSON")

    search_criteria = request.get_json()
    states_list = search_criteria.get('states', [])
    cities_list = search_criteria.get('cities', [])
    amenities_list = search_criteria.get('amenities', [])

    found_places = set()

    if not states_list and not cities_list and not amenities_list:
        found_places.update(storage.all(Place).values())

    if states_list:
        for state_id in states_list:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        if not amenities_list or all(amenity in place.amenities for amenity in amenities_list):
                            found_places.add(place)

    if cities_list:
        for city_id in cities_list:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if not amenities_list or all(amenity in place.amenities for amenity in amenities_list):
                        found_places.add(place)

    if amenities_list and not states_list and not cities_list:
        all_places = storage.all(Place).values()
        for place in all_places:
            if all(amenity in place.amenities for amenity in amenities_list):
                found_places.add(place)

    return jsonify([place.to_dict() for place in found_places])

@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = [place.to_dict() for place in city.places]
    return jsonify(all_places)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
