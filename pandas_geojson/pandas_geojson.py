import json
from urllib.request import urlopen

def to_geojson(df, lat, lon, properties):

    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}}

        feature['geometry']['coordinates'] = [row[lon], row[lat]]

        for prop in properties:
            feature['properties'][prop] = row[prop]

        geojson['features'].append(feature)

    return geojson

def write_geojson(geo_json, filename, indent=None):
    geo_json_data = json.dumps(geo_json, indent=indent)
    with open(filename, 'w', encoding='utf8') as f:
        f.write(geo_json_data)


def filter_geojson(geo_json, filter_list, property_key):
    filtered = []
    for ft in geo_json['features']:
        if ft['properties'][f'{property_key}'] in filter_list:
            filtered.append(ft)
    # print(len(filtered))

    newgeojson = {}
    newgeojson['type'] = 'FeatureCollection'
    newgeojson['features'] = filtered
    newgeojson = json.dumps(newgeojson)

    return newgeojson

def read_geojson(filename):
    with open(f'{filename}') as response:
        geo_json = json.load(response)
    return geo_json

def read_geojson_url(url):
    with urlopen(f'{url}') as response:
        geo_json = json.load(response)

    return geo_json