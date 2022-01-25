import geojson

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

    def write_geojson(self,df,filename):
        with open(filename, 'w', encoding='utf8') as f:
            geojson.dump(df, f, sort_keys=True, ensure_ascii=False)
