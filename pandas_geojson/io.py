from pandas import DataFrame
from pandas_geojson.core import GeoJSON
import json
from urllib.request import urlopen


def save_geojson(geojson: GeoJSON, filename: str, indent=None):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(geojson.to_dict(), f, indent=indent)

def read_geojson(file_path: str) -> GeoJSON:
    with open(file_path) as response:
        geo_json_data = json.load(response)
    return GeoJSON.from_dict(geo_json_data)

def read_geojson_url(url: str) -> GeoJSON:
    with urlopen(url) as response:
        geo_json_data = json.load(response)
    return GeoJSON.from_dict(geo_json_data)