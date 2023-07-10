
import random
import json
min_latitude,max_latitude,max_longitude,min_longitude = (40.882214, 40.680396, -73.907000, -74.047285)



def random_point(min_longitude, max_longitude, min_latitude, max_latitude):
    longitude = random.uniform(min_longitude, max_longitude)
    latitude = random.uniform(min_latitude, max_latitude)
    return [longitude, latitude]

taxi_count = 50
passenger_count = 200

features = []

for i in range(taxi_count):
    point = random_point(min_longitude, max_longitude, min_latitude, max_latitude)
    features.append({
        "type": "Feature",
        "properties": {"icon": "taxi"},
        "geometry": {
            "type": "Point",
            "coordinates": point
        }
    })

for i in range(passenger_count):
    point = random_point(min_longitude, max_longitude, min_latitude, max_latitude)
    features.append({
        "type": "Feature",
        "properties": {"icon": "passenger"},
        "geometry": {
            "type": "Point",
            "coordinates": point
        }
    })

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

with open("taxi_and_passengers.geojson", "w") as f:
    json.dump(geojson_data, f)