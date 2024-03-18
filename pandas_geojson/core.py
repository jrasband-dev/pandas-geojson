from dataclasses import dataclass, field
from typing import List, Any, Dict
import pandas as pd
import json

@dataclass
class GeoJSONFeature:
    type: str
    geometry: Dict[str, Any]
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GeoJSON:
    type: str = 'FeatureCollection'
    features: List[GeoJSONFeature] = field(default_factory=list)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def add_feature(self, feature_type: str, coordinates: Any = [], properties: dict = {}):
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
        features = [GeoJSONFeature(**feature) for feature in data['features']]
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

    
