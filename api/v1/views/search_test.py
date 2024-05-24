class Place:
    def __init__(self, id, name, amenities):
        self.id = id
        self.name = name
        self.amenities = amenities

    def __repr__(self):
        return f"Place(id={self.id}, name='{self.name}', amenities={self.amenities})"

class City:
    def __init__(self, id, name, places):
        self.id = id
        self.name = name
        self.places = places

class State:
    def __init__(self, id, name, cities):
        self.id = id
        self.name = name
        self.cities = cities

# Creating mock data
places = [
    Place(id="place_0", name="Place 0 in Cairo", amenities=["wifi", "pool"]),
    Place(id="place_1", name="Place in Giza", amenities=["wifi"]),
    Place(id="place_2", name="Place 2 in Cairo", amenities=["pool"])
]

cities = {
    "city_1": City(id="city_1", name="Cairo", places=[places[0], places[2]]),
    "city_2": City(id="city_2", name="Giza", places=[places[1]])
}

states = {
    "state_1": State(id="state_1", name="Cairo", cities=[cities["city_1"]]),
    "state_2": State(id="state_2", name="Giza", cities=[cities["city_2"]])
}

def search_places(states_list, cities_list, amenities_list):
    found_places = set()

    if not states_list and not cities_list and not amenities_list:
        # If no criteria specified, return all places
        return [place for city in cities.values() for place in city.places]

    if states_list:
        for state_id in states_list:
            state = states.get(state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        if not amenities_list or all(amenity in place.amenities for amenity in amenities_list):
                            found_places.add(place)

    if cities_list:
        for city_id in cities_list:
            city = cities.get(city_id)
            if city:
                for place in city.places:
                    if not amenities_list or all(amenity in place.amenities for amenity in amenities_list):
                        found_places.add(place)

    if amenities_list and not states_list and not cities_list:
        # Filter all places by amenities if no city or state is specified
        for city in cities.values():
            for place in city.places:
                if all(amenity in place.amenities for amenity in amenities_list):
                    found_places.add(place)

    return list(found_places)

# Example test call
test_places = search_places(states_list=[], cities_list=[], amenities_list=["pool"])
print(test_places)
