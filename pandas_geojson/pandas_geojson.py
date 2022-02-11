import json
from urllib.request import urlopen

class GeoJSON():
    def to_geojson(self, df, lat, lon, properties):

        geojson = {'type': 'FeatureCollection', 'features': []}
        for _, row in df.iterrows():
            # create a feature template to fill in
            feature = {'type': 'Feature',
                       'properties': {},
                       'geometry': {'type': 'Point',
                                    'coordinates': []}}

            # fill in the coordinates
            feature['geometry']['coordinates'] = [row[lon], row[lat]]

            # for each column, get the value and add it as a new feature property
            for prop in properties:
                feature['properties'][prop] = row[prop]

            # add this feature (aka, converted dataframe row) to the list of features inside our dict
            geojson['features'].append(feature)

        return geojson

    def write_geojson(self, geo_json, filename):
        with open(filename, 'w', encoding='utf8') as f:
            f.write(geo_json)
            
            
    def filter_geojson(self,geo_json, filter_list, property_key):
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

    def read_geojson(self,filename):
        with open(f'{filename}') as response:
            geo_json = json.load(response)
        return geo_json

    def read_geojson_url(self, url):
        with urlopen(f'{url}') as response:
            geo_json = json.load(response)

        return geo_json