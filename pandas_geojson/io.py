from pandas import DataFrame
from pandas_geojson.core import GeoJSON
import json
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from pandas_geojson.parsers.kml import parse_kml_placemarks


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

def read_kml(file_path: str) -> GeoJSON:
    """
    Convert KML file to GeoJSON format using GeoJSON object.
    file_path (str): Path to the KML file.

    Returns:
    GeoJSON: GeoJSON object representing the contents of the KML file.
    """


    # Parse KML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Initialize GeoJSON object
    geojson_data = GeoJSON()

    # Parse placemarks
    placemarks = parse_kml_placemarks(root)

    # Add placemarks to GeoJSON features
    geojson_data.add_features(placemarks)

    return geojson_data