![](https://raw.githubusercontent.com/jrasband-dev/pandas-geojson/master/static/pandasgeojson.png)

---
![PyPI - Version](https://img.shields.io/pypi/v/pandas-geojson)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pandas-geojson)
![PyPI - License](https://img.shields.io/pypi/l/pandas-geojson)
![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/pandas-geojson)


# Getting Started
Install the latest version of pandas-geojson using pip.
```
pip install pandas-geojson
```



## Open GeoJSON Files
Using the `read_geojson` function, you can easily read in GeoJSON data int the GeoJSON object. 



```python
import pandas_geojson as pdg
geojson = pdg.read_geojson('datasets/National_Obesity_By_State.geojson')
geojson
```

## List Properties
Pandas-GeoJSON utilizes properties to filter large geojson files. This functionallity helps you identify all of the properties in the geojson file so that you can choose a filter criteria. For more on filtering see [filter_geojson](#filter-geojson)


```python
geojson.get_properties()
```

## DataFrame to GeoJSON

Pandas-GeoJSON makes it easy to convert a dataframe with coordinates into a GeoJSON object. Your DataFrame **must** contain at least two columns with the following information:
* Geometry Type
* Coodinates

If you have properties in your DataFrame that you want to include, you can add those as well. If you don't have you own file, feel free to use the example csv file in the repo.


```python
import pandas as pd
import json
csv = pd.read_csv('datasets/ObesityByState.csv')
csv.head()
```


```python
import pandas_geojson as pdg
geojson = pdg.GeoJSON.from_dataframe(csv
                                     ,geometry_type_col='type'
                                     ,coordinate_col='coordinates'
                                     ,property_col_list=['FID','NAME','Obesity']
                                     )
geojson
```

## GeoJSON to DataFrame

You can convert your GeoJSON object to a dataframe using the `to_dataframe` function. This will return a normalized dataframe of your GeoJSON data. From here you can manipulate, filter, and save your dataframe. 


```python
import pandas_geojson as pdg

geojson = pdg.read_geojson('datasets/National_Obesity_By_State.geojson')
df = geojson.to_dataframe()
df.head()
```

## Filter GeoJSON
GeoJSON files can be large and complex. Pandas-GeoJSON gives you the ability to filter geojson data. 

You can filter based on properties in the file. The `filter_geojson` function asks for a property key and a list of property values to filter on. The function will return a new GeoJSON object with only the values passed into the list. You can only use one property key at a time to filter. 



```python
import pandas_geojson as pdg
geojson = pdg.read_geojson('datasets/National_Obesity_By_State.geojson')
properties = geojson.get_properties()
properties

```


```python
new_geojson = geojson.filter_geojson(property_values=['Colorado'],property_key='NAME')
new_geojson
```

## Export GeoJSON

Once you've filtered your GeoJSON object you can easily export it as a new GeoJSON file using the `save_geojson` function. 


```python
pdg.save_geojson(new_geojson,'Filtered.geojson',indent=4)
```

## Creating GeoJSON

How about creating a GeoJSON object from scratch? You can do this programmically through the package. Below is an example of how to create an empty GeoJSON object.


```python
import pandas_geojson as pdg
geojson = pdg.GeoJSON()
geojson
```




    {
        "type": "FeatureCollection",
        "features": []
    }




```python
from pandas_geojson.core import Point
point = Point(geometry=[-105.63012379499997, 32.971263161000024],properties={'ID':1})
point
```




    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                -105.63012379499997,
                32.971263161000024
            ]
        },
        "properties": {
            "ID": 1
        }
    }




```python
from pandas_geojson.core import MultiPoint
multipoint = MultiPoint(geometry=[[-105.63012379499997, 32.971263161000024], [-105.63012379499997, 32.971263161000024]])
multipoint
```




    {
        "type": "Feature",
        "geometry": {
            "type": "MultiPoint",
            "coordinates": [
                [
                    -105.63012379499997,
                    32.971263161000024
                ],
                [
                    -105.63012379499997,
                    32.971263161000024
                ]
            ]
        },
        "properties": {}
    }




```python
from pandas_geojson.core import LineString
line = LineString(geometry=[[-105.63012379499997, 32.971263161000024],[-105.6,30.26]],properties={'ID':1})
line

```




    {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [
                    -105.63012379499997,
                    32.971263161000024
                ],
                [
                    -105.6,
                    30.26
                ]
            ]
        },
        "properties": {
            "ID": 1
        }
    }




```python
from pandas_geojson.core import MultiLineString
multiline = MultiLineString(geometry=[[[-73.989, 40.752], [-74.008, 40.722], [-73.985, 40.706]],[[-73.987, 40.754], [-73.981, 40.743], [-73.974, 40.735]]],properties={'ID':1})
multiline 
```




    {
        "type": "Feature",
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [
                [
                    [
                        -73.989,
                        40.752
                    ],
                    [
                        -74.008,
                        40.722
                    ],
                    [
                        -73.985,
                        40.706
                    ]
                ],
                [
                    [
                        -73.987,
                        40.754
                    ],
                    [
                        -73.981,
                        40.743
                    ],
                    [
                        -73.974,
                        40.735
                    ]
                ]
            ]
        },
        "properties": {
            "ID": 1
        }
    }




```python
from pandas_geojson.core import Polygon
polygon = Polygon(geometry=[[[-10.0, 10.0], [-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, 10.0]]]
                    ,properties={'ID':1}
                    )
polygon
```




    {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -10.0,
                        10.0
                    ],
                    [
                        -10.0,
                        -10.0
                    ],
                    [
                        10.0,
                        -10.0
                    ],
                    [
                        10.0,
                        10.0
                    ],
                    [
                        -10.0,
                        10.0
                    ]
                ]
            ]
        },
        "properties": {
            "ID": 1
        }
    }




```python
from pandas_geojson.core import MultiPolygon
multipolygon = MultiPolygon(geometry=[[[[-10.0, 10.0], [-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, 10.0]]],[[[-20.0, 20.0], [-20.0, -20.0], [20.0, -20.0], [20.0, 20.0],[-20.0, 20.0]]]]
                    ,properties={'ID':1}
                    )
multipolygon
```




    {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [
                            -10.0,
                            10.0
                        ],
                        [
                            -10.0,
                            -10.0
                        ],
                        [
                            10.0,
                            -10.0
                        ],
                        [
                            10.0,
                            10.0
                        ],
                        [
                            -10.0,
                            10.0
                        ]
                    ]
                ],
                [
                    [
                        [
                            -20.0,
                            20.0
                        ],
                        [
                            -20.0,
                            -20.0
                        ],
                        [
                            20.0,
                            -20.0
                        ],
                        [
                            20.0,
                            20.0
                        ],
                        [
                            -20.0,
                            20.0
                        ]
                    ]
                ]
            ]
        },
        "properties": {
            "ID": 1
        }
    }



## Adding Features

You can add features to a GeoJSON object in two ways:
* `add_features`: allows you to add previously created Feature objects in bulk. 
* `add_feature`: allows you to add a single feature




```python
geojson.add_features([point, multipoint,line,multiline,polygon,multipolygon])
geojson
```




    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -105.63012379499997,
                        32.971263161000024
                    ]
                },
                "properties": {
                    "ID": 1
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiPoint",
                    "coordinates": [
                        [
                            -105.63012379499997,
                            32.971263161000024
                        ],
                        [
                            -105.63012379499997,
                            32.971263161000024
                        ]
                    ]
                },
                "properties": {}
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            -105.63012379499997,
                            32.971263161000024
                        ],
                        [
                            -105.6,
                            30.26
                        ]
                    ]
                },
                "properties": {
                    "ID": 1
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [
                            [
                                -73.989,
                                40.752
                            ],
                            [
                                -74.008,
                                40.722
                            ],
                            [
                                -73.985,
                                40.706
                            ]
                        ],
                        [
                            [
                                -73.987,
                                40.754
                            ],
                            [
                                -73.981,
                                40.743
                            ],
                            [
                                -73.974,
                                40.735
                            ]
                        ]
                    ]
                },
                "properties": {
                    "ID": 1
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -10.0,
                                10.0
                            ],
                            [
                                -10.0,
                                -10.0
                            ],
                            [
                                10.0,
                                -10.0
                            ],
                            [
                                10.0,
                                10.0
                            ],
                            [
                                -10.0,
                                10.0
                            ]
                        ]
                    ]
                },
                "properties": {
                    "ID": 1
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [
                                    -10.0,
                                    10.0
                                ],
                                [
                                    -10.0,
                                    -10.0
                                ],
                                [
                                    10.0,
                                    -10.0
                                ],
                                [
                                    10.0,
                                    10.0
                                ],
                                [
                                    -10.0,
                                    10.0
                                ]
                            ]
                        ],
                        [
                            [
                                [
                                    -20.0,
                                    20.0
                                ],
                                [
                                    -20.0,
                                    -20.0
                                ],
                                [
                                    20.0,
                                    -20.0
                                ],
                                [
                                    20.0,
                                    20.0
                                ],
                                [
                                    -20.0,
                                    20.0
                                ]
                            ]
                        ]
                    ]
                },
                "properties": {
                    "ID": 1
                }
            }
        ]
    }




```python

```


```python

```
