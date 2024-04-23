from dataclasses import dataclass, field
from typing import List, Any, Dict, Union
import pandas as pd
import json

@dataclass
class Point:
    '''
    GeoJSON Compliant Point Geometry 
    '''
    type: str = 'Point'
    geometry: List[float] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __post_init__(self):
        self.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'geometry': self.geometry,
            'properties': self.properties
        }

    def validate(self):
        if self.type != "Point":
            raise ValueError("Type must be 'Point' for Point geometry.")
        if len(self.geometry) != 2:
            raise ValueError("Point must have a single pair of coordinates (latitude and longitude).")
        if not all(isinstance(coord, (int, float)) for coord in self.geometry):
            raise ValueError("Coordinates must be numerical values.")

@dataclass
class MultiPoint:
    '''
    GeoJSON Compliant MultiPoint Geometry 
    '''
    type: str = 'MultiPoint'
    geometry: List[List[float]] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __post_init__(self):
        self.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'geometry': self.geometry,
            'properties': self.properties
        }    

    def validate(self):
        if self.type != "MultiPoint":
            raise ValueError("Type must be 'MultiPoint' for MultiPoint geometry.")
        if not isinstance(self.geometry, list) or len(self.geometry) < 2 or not all(isinstance(coord, list) and len(coord) == 2 for coord in self.geometry):
            raise ValueError("MultiPoint must have at least two pairs of coordinates.")

@dataclass
class LineString:
    '''
    GeoJSON Compliant LineString Geometry 
    '''
    type: str = 'LineString'
    geometry: List[List[float]] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __post_init__(self):
        self.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'geometry': self.geometry,
            'properties': self.properties
        }    

    def validate(self):
        if self.type != "LineString":
            raise ValueError("Type must be 'LineString' for LineString geometry.")
        if not isinstance(self.geometry, list) or len(self.geometry) < 2 or not all(isinstance(coord, list) and len(coord) == 2 for coord in self.geometry):
            raise ValueError("LineString must have a list of coordinate pairs with at least two coordinates.")

@dataclass
class MultiLineString:
    '''
    GeoJSON Compliant MultiLineString Geometry 
    '''
    type: str = 'MultiLineString'
    geometry: List[List[List[float]]] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __post_init__(self):
        self.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'geometry': self.geometry,
            'properties': self.properties
        }    

    def validate(self):
        if self.type != "MultiLineString":
            raise ValueError("Type must be 'MultiLineString' for MultiLineString geometry.")
        if len(self.geometry) < 2:
            raise ValueError("MultiLineString must have at least two LineString geometries.")
        for line_string in self.geometry:
            if len(line_string) < 2:
                raise ValueError("Each LineString in MultiLineString must have at least two coordinates.")
            for point in line_string:
                if len(point) != 2:
                    raise ValueError("Each point in MultiLineString geometry must have exactly two coordinates (longitude and latitude).")

@dataclass
class Polygon:
    '''
    GeoJSON Compliant Polygon Geometry 
    '''
    type: str = 'Polygon'
    geometry: List[List[List[float]]] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __post_init__(self):
        self.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'geometry': self.geometry,
            'properties': self.properties
        }    

    def validate(self):
        if self.type != "Polygon":
            raise ValueError("Type must be 'Polygon' for Polygon geometry.")
        if len(self.geometry) < 4:
            raise ValueError("Polygon must have at least four coordinates (outer ring).")
        for coords in self.geometry:
            if len(coords) < 2:
                raise ValueError("Each coordinate sublist must contain at least two elements.")
        if self.geometry[0] != self.geometry[-1]:
            raise ValueError("First and last points of the geometry must be the same.")

@dataclass
class MultiPolygon:
    '''
    GeoJSON Compliant MutliPolygon Geometry 
    '''
    type: str = 'MultiPolygon'
    geometry: List[List[List[List[float]]]] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __post_init__(self):
        self.validate()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'geometry': self.geometry,
            'properties': self.properties
        }   

    def validate(self):
        if self.type != "MultiPolygon":
            raise ValueError("Type must be 'MultiPolygon' for MultiPolygon geometry.")
        if len(self.geometry) < 2:
            raise ValueError("MultiPolygon must have at least two polygons.")

        for polygon in self.geometry:
            if len(polygon) < 1:
                raise ValueError("Each Polygon in MultiPolygon must have at least one ring.")
            for ring in polygon:
                if len(ring) < 4 or ring[0] != ring[-1]:
                    raise ValueError("Each ring in MultiPolygon must have at least four coordinates and be closed.")

@dataclass
class GeoJSONFeature:
    type: str
    geometry: Dict[str, Any] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GeoJSON:
    '''
    Main Object for GeoJSON data. 
    '''
    type: str = 'FeatureCollection'
    features: List[Union[GeoJSONFeature,Point,MultiPoint,LineString,MultiLineString,Polygon,MultiPolygon]] = field(default_factory=list)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)
    
    def add_features(self, feature_list: List[Union[GeoJSONFeature,Point,MultiPoint,LineString,MultiLineString,Polygon,MultiPolygon]]):
        '''
        Add Multiple Features at once
        '''

        self.features.extend(feature_list)

    def add_feature(self, feature_type: str, coordinates: Any = [], properties: dict = {}):
        '''
        Allows you to add features to the GeoJSON object.
        '''
        geometry = {'type': feature_type, 'coordinates': coordinates}
        feature = GeoJSONFeature(type='Feature', geometry=geometry, properties=properties)
        self.features.append(feature)

    def get_properties(self) -> List[str]:
        properties = list(self.features[0].properties.keys()) if self.features else []
        return properties

    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type,
            'features': [feature.__dict__ for feature in self.features]
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        data = pd.json_normalize(self.to_dict(), record_path=['features'])
        return data
    
    def filter_geojson(self, property_values: List[str], property_key: str) -> 'GeoJSON':
        '''
        Filters GeoJSON features based on values in properties object.

        :return: GeoJSON
        '''
        filtered_features = [feature for feature in self.features if feature.properties.get(property_key) in property_values]
        return GeoJSON(type='FeatureCollection', features=filtered_features)
    

    @classmethod
    def from_dict(cls, data):
        features = []
        for feature_data in data['features']:
            properties = feature_data.get('properties', {})
            feature = GeoJSONFeature(type='Feature', geometry=feature_data['geometry'], properties=properties)
            features.append(feature)
        return cls(type=data['type'], features=features)
    
    @classmethod
    def from_dataframe(cls
                       ,df
                       ,geometry_type_col: str = 'geometry.type'
                       ,coordinate_col: str = 'geometry.coordinates'
                       ,property_col_list: List[str] = []
                       ):
        geojson = cls(type='FeatureCollection')
        for _, row in df.iterrows():
            coordinates = row[coordinate_col]
            geometry = {'type': row[geometry_type_col], 'coordinates': coordinates}
            properties = {col: row[col] for col in property_col_list}
            feature = GeoJSONFeature(type='Feature', geometry=geometry, properties=properties)
            geojson.features.append(feature)
        return geojson
    
    @classmethod
    def from_coordinates(cls, df, lat: str, lon: str, properties: List[str]) -> 'GeoJSON':
        geojson = cls(type='FeatureCollection')
        for _, row in df.iterrows():
            coordinates = [row[lon], row[lat]]
            feature_properties = {prop: row[prop] for prop in properties}
            feature = GeoJSONFeature(type='Point', coordinates=coordinates, properties=feature_properties)
            geojson.features.append(feature)
        return geojson

    
