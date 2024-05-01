from dataclasses import dataclass, field
from typing import List, Any, Dict, Union
import pandas as pd
import json


@dataclass
class Geometry:
    '''
    Base class for GeoJSON compliant geometries
    '''
    geometry: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.type = self.__class__.__name__
        if self.geometry:
            self.geometry['type'] = self.type
            self.validate()

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Feature',
            'geometry': self.geometry,
            'properties': self.properties if self.properties else {}   
        }

    def validate(self):
        raise NotImplementedError("Validation method must be implemented in subclasses.")

@dataclass
class Point(Geometry):
    '''
    GeoJSON Compliant Point Geometry 
    '''
    def __init__(self, geometry: Dict[str, Any], properties: Dict[str, Any] = None):
        super().__init__(geometry={'type': 'Point', 'coordinates': geometry}, properties=properties)
    
    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)
    

    def validate(self):
        if self.geometry:
            if self.geometry.get('type') != "Point":
                raise ValueError("Geometry type must be 'Point' for Point geometry.")
            coordinates = self.geometry.get('coordinates', [])
            if not isinstance(coordinates, list) or len(coordinates) != 2:
                raise ValueError("Coordinates must be provided as a list of two numerical values (longitude and latitude).")
            if not all(isinstance(coord, (int, float)) for coord in coordinates):
                raise ValueError("Coordinates must be numerical values.")

@dataclass
class MultiPoint(Geometry):
    '''
    GeoJSON Compliant MultiPoint Geometry 
    '''
    def __init__(self, geometry: List[List[float]], properties: Dict[str, Any] = None):
        super().__init__(geometry={'type': 'MultiPoint', 'coordinates': geometry}, properties=properties)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def validate(self):
        if self.geometry:
            if self.geometry.get('type') != "MultiPoint":
                raise ValueError("Geometry type must be 'MultiPoint' for MultiPoint geometry.")
            coordinates = self.geometry.get('coordinates', [])
            if not isinstance(coordinates, list) or not all(isinstance(coord, list) and len(coord) == 2 for coord in coordinates):
                raise ValueError("Each coordinate pair in MultiPoint geometry must contain two elements (longitude and latitude).")

@dataclass
class LineString(Geometry):
    '''
    GeoJSON Compliant LineString Geometry 
    '''
    def __init__(self, geometry: List[List[float]], properties: Dict[str, Any] = None):
        super().__init__(geometry={'type': 'LineString', 'coordinates': geometry}, properties=properties)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def validate(self):
        if self.geometry:
            if self.geometry.get('type') != "LineString":
                raise ValueError("Geometry type must be 'LineString' for LineString geometry.")
            coordinates = self.geometry.get('coordinates', [])
            if not isinstance(coordinates, list) or not all(isinstance(coord, list) and len(coord) == 2 for coord in coordinates):
                raise ValueError("Each coordinate pair in LineString geometry must contain two elements (longitude and latitude).")

@dataclass
class MultiLineString(Geometry):
    '''
    GeoJSON Compliant MultiLineString Geometry 
    '''
    def __init__(self, geometry: List[List[List[float]]], properties: Dict[str, Any] = None):
        super().__init__(geometry={'type': 'MultiLineString', 'coordinates': geometry}, properties=properties)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def validate(self):
        if self.geometry:
            if self.geometry.get('type') != "MultiLineString":
                raise ValueError("Geometry type must be 'MultiLineString' for MultiLineString geometry.")
            for line_string in self.geometry.get('coordinates', []):
                if not isinstance(line_string, list) or not all(isinstance(coord, list) and len(coord) == 2 for coord in line_string):
                    raise ValueError("Each coordinate pair in MultiLineString geometry must contain two elements (longitude and latitude).")

@dataclass
class Polygon(Geometry):
    '''
    GeoJSON Compliant Polygon Geometry 
    '''
    def __init__(self, geometry: List[List[List[float]]], properties: Dict[str, Any] = None):
        super().__init__(geometry={'type': 'Polygon', 'coordinates': geometry}, properties=properties)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def validate(self):
        if self.geometry:
            if self.geometry.get('type') != "Polygon":
                raise ValueError("Geometry type must be 'Polygon' for Polygon geometry.")
            for ring in self.geometry.get('coordinates', []):
                if not isinstance(ring, list) or not all(isinstance(coord, list) and len(coord) == 2 for coord in ring):
                    raise ValueError("Each coordinate pair in Polygon geometry must contain two elements (longitude and latitude).")

@dataclass
class MultiPolygon(Geometry):
    '''
    GeoJSON Compliant MultiPolygon Geometry 
    '''
    def __init__(self, geometry: List[List[List[List[float]]]], properties: Dict[str, Any] = None):
        super().__init__(geometry={'type': 'MultiPolygon', 'coordinates': geometry}, properties=properties)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def validate(self):
        if self.geometry:
            if self.geometry.get('type') != "MultiPolygon":
                raise ValueError("Geometry type must be 'MultiPolygon' for MultiPolygon geometry.")
            for polygon in self.geometry.get('coordinates', []):
                for ring in polygon:
                    if not isinstance(ring, list) or not all(isinstance(coord, list) and len(coord) == 2 for coord in ring):
                        raise ValueError("Each coordinate pair in MultiPolygon geometry must contain two elements (longitude and latitude).")


@dataclass
class GeoJSON:
    '''
    Main Object for GeoJSON data. 
    '''
    type: str = 'FeatureCollection'
    features: List[Union[Point,MultiPoint,LineString,MultiLineString,Polygon,MultiPolygon]] = field(default_factory=list)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def __iter__(self):
        return iter(self.features)
    
    def add_features(self, feature_list: List[Union[Point,MultiPoint,LineString,MultiLineString,Polygon,MultiPolygon]]):
        '''
        Add Multiple Features at once
        '''
        instantiated_features = []
        for feature in feature_list:
            # Instantiate the class if it's not already an instance
            if not isinstance(feature, (Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon)):
                print(f"Invalid feature type: {type(feature)}")
                raise ValueError("Each feature must be a geometry subclasses.")
            instantiated_features.append(feature.to_dict())
        self.features.extend(instantiated_features)


    def get_properties(self) -> List[str]:
        properties = list(self.features[0]['properties'].keys()) if self.features else []
        return properties

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'features': self.features
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        data = pd.json_normalize(self.to_dict(), record_path=['features'])
        return data
    
    def filter_geojson(self, property_values: List[str], property_key: str) -> 'GeoJSON':
        '''
        Filters GeoJSON features based on values in properties object.

        :return: GeoJSON
        '''
        # for feature in self.features:
        #     print(feature)

        filtered_features = []
        for feature in self.features:
            if feature['properties'].get(property_key) in property_values:
                filtered_features.append(feature)  
        return GeoJSON(type='FeatureCollection', features=filtered_features)

    
    @classmethod
    def from_dict(self, data):
        features = []
        for feature_data in data['features']:
            properties = feature_data.get('properties', {})
            geometry_data = feature_data['geometry']

            if geometry_data is None:
                # Skip this feature if geometry data is missing
                continue

            geometry_type = geometry_data['type']
            geometry_coordinates = geometry_data['coordinates']

            geometry_class = {
                "Point": Point,
                "MultiPoint": MultiPoint,
                "LineString": LineString,
                "MultiLineString": MultiLineString,
                "Polygon": Polygon,
                "MultiPolygon": MultiPolygon
            }.get(geometry_type)

            if geometry_class is None:
                raise ValueError(f"Invalid geometry type: {geometry_type}")
                
            geometry_instance = geometry_class(geometry=geometry_coordinates, properties=properties)
            features.append(geometry_instance.to_dict())

        return self(type='Feature Collection', features=features)
    
    @classmethod
    def from_dataframe(cls,
                    df,
                    geometry_type_col: str = 'geometry.type',
                    coordinate_col: str = 'geometry.coordinates',
                    property_col_list: List[str] = []):
        
        geojson = cls(type='FeatureCollection')

        for _, row in df.iterrows():
            coordinates = row[coordinate_col]
            geometry = {'type': row[geometry_type_col], 'coordinates': coordinates}
            properties = {col: row[col] for col in property_col_list}
            # Construct the feature directly as a dictionary
            feature = {
                'type': 'Feature',
                'geometry': geometry,
                'properties': properties
            }
            geojson.features.append(feature)

        return geojson


    
