![](https://raw.githubusercontent.com/jaycroft/pandas-geojson/master/static/pandasgeojson.png)

---

## Features
* Convert DataFame with Lat Long Coordinates to GeoJSON
* Write & Save GeoJSON files
* Open GeoJSON from file or url
* Filter GeoJSON based on list criteria

## Getting Started
Install the latest version of pandas-geojson using pip.
```
pip install pandas-geojson
```

## Converting DataFrames to GeoJSON
To use this first function, you will need a csv file with latitude and lognitude coordinates. If you do not have one to use, there is a sample CSV in the Repo. Use pandas to read in your data.

INPUT
```
import pandas as pd
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
Definie your variable and call the to_geojson function. You will need to pass your dataframe object and specify the lat and long cordinate columns. You can also pass a list with the properties you want to include (essentially the meta data of the coordinates).


INPUT
```
from pandas_geojson import to_geojson
geo_json = to_geojson(df=data, lat='lat', lon='long',
                 properties=['name','marker-symbol','marker-color'])
print(geo_json)
```
OUTPUT
```
{'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-111.85528049999999, 48.70207631]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-111.90390740000001, 46.768476899999996]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-112.90390740000001, 49.768476899999996]}}, {'type': 'Feature', 'properties': {'name': 'Random', 'marker-symbol': 'star', 'marker-color': '#C91313'}, 'geometry': {'type': 'Point', 'coordinates': [-110.90390740000001, 45.768476899999996]}}]}
```
## Opening GeoJSON
There are two functions for opening geojson files. The first function opens it from a URL, the second opens from files on your local computer. 

```
from pandas_geojson import read_geojson_url
geo_json = read_geojson_url('<URL>')
```
OR
```
from pandas_geojson import read_geojson
geo_json = read_geojson('<FILENAME>')
```
## Saving GeoJSON Files
The save function has two required arguements. The first is the geojson object. The second is the filename. Adding indentation and formatting is optional, but is useful for saving geojson in an easy-to-read format. 

INPUT
```
from pandas_geojson import write_geojson
write_geojson(geo_json, filename='random.geojson', indent=4)
```
OUTPUT
```
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Randomize",
                "marker-symbol": "star",
                "marker-color": "#C91313"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -111.8552805,
                    48.70207631
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Random",
                "marker-symbol": "star",
                "marker-color": "#C91313"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -111.9039074,
                    46.7684769
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Random",
                "marker-symbol": "star",
                "marker-color": "#C91313"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -112.9039074,
                    49.7684769
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Randomize",
                "marker-symbol": "star",
                "marker-color": "#C91313"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -110.9039074,
                    45.7684769
                ]
            }
        }
    ]
}
```
## Filtering GeoJSON
GeoJSON files can be large and complex. Filtering to what is important is a useful tool. To use this function you need to have a list of the items you want to filter to. Once you have that, load your geojson file using the read_geojson function shown above. Set you output variable name and then call the filter_geojson function. Pass your geojson object and filter list. Finally, you will need a property key to identify where to look for the items in your list. After running the code, you should get a new filtered geojson object.

INPUT
```
from pandas_geojson import read_geojson, filter_geojson
filter = ['Randomize']
geojson = read_geojson('random.geojson')
output = filter_geojson(geo_json=geojson, filter_list=filter, property_key='name')
print(output)
```
OUTPUT
```
{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "Randomize", "marker-symbol": "star", "marker-color": "#C91313"}, "geometry": {"type": "Point", "coordinates": [-111.8552805, 48.70207631]}}, {"type": "Feature", "properties": {"name": "Randomize", "marker-symbol": "star", "marker-color": "#C91313"}, "geometry": {"type": "Point", "coordinates": [-110.9039074, 45.7684769]}}]}
```
