# pandas-geojson
This library contains: 
* Functions for converting pandas dataframes to GeoJSON format.
* A write function to convert GeoJSON objeccts into geojson files.

```
pip install pandas-geojson
```

## Getting Started
```
>>> from pandas_geojson.GeoJSON import GeoJSON
>>> import pandas as pd
>>> gjson = GeoJSON()
>>> data = pd.read_csv('Test.csv')
>>> print(data.head())

     name        lat        long marker-symbol marker-color
0  Random  48.702076 -111.855280          star      #C91313
1  Random  46.768477 -111.903907          star      #C91313
2  Random  49.768477 -112.903907          star      #C91313
3  Random  45.768477 -110.903907          star      #C91313

>>> geo = gjson.to_geojson(df=data, lat='lat', lon='long',
                 properties=['name','marker-symbol','marker-color'])
>>> print(geo)

{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-111.85528049999999, 48.70207631]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-111.90390740000001, 46.768476899999996]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-112.90390740000001, 49.768476899999996]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-110.90390740000001, 45.768476899999996]}}]}
```

## Saving GeoJSON
```
>>> gjson.write_geojson(geo, 'Test.geojson')
```
