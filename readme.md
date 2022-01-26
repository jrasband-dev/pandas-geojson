# pandas-geojson
This library contains: 
* Convert DataFame to GeoJSON
* Write GeoJSON to convert GeoJSON objeccts into geojson files.
* Open GeoJSON options from file or url
* Filter GeoJSON

```
pip install pandas-geojson
```

## Converting DataFrames to GeoJSON
INPUT
```
from pandas_geojson.GeoJSON import GeoJSON
import pandas as pd
gjson = GeoJSON()
data = pd.read_csv('Test.csv')
print(data.head())
```
OUTPUT
```
     name        lat        long marker-symbol marker-color
0  Random  48.702076 -111.855280          star      #C91313
1  Random  46.768477 -111.903907          star      #C91313
2  Random  49.768477 -112.903907          star      #C91313
3  Random  45.768477 -110.903907          star      #C91313
```
INPUT
```
geo_json = gjson.to_geojson(df=data, lat='lat', lon='long',
                 properties=['name','marker-symbol','marker-color'])
print(geo_json)
```
OUTPUT
```
{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-111.85528049999999, 48.70207631]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-111.90390740000001, 46.768476899999996]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-112.90390740000001, 49.768476899999996]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-110.90390740000001, 45.768476899999996]}}]}
```
## Opening GeoJSON
```
geo_json = gjson.read_geojson_url('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json')
```
OR
```
geo_json = gjson.read_geojson('FIPS_Counties.geojson')
```
## Saving GeoJSON
```
gjson.write_geojson(geo_json, 'Test.geojson')
```

## Filtering GeoJSON
Sometimes you want to filter existing GeoJSON datasets to only include specific locations. This function accomplishes that. 
```
data = pd.read_csv('filter.csv')
lid_zips = data['FIPS'].astype(str).to_list()
counties = gjson.read_geojson('FIPS_Counties.geojson')
geo_json = gjson.filter_geojson(geo_json=counties, filter_list=lid_zips, property_key='GEO_ID')
print(geo_json)
```