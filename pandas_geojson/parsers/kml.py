from pandas_geojson.core import GeoJSON, Point, LineString, Polygon

def parse_kml_placemarks(root):
    """
    Parse KML placemarks recursively.

    Args:
    root (Element): Root element of the KML document.

    Returns:
    GeoJSON: GeoJSON object representing placemarks.
    """
    geojson = GeoJSON()
    features = []

    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        feature_properties = {}

        # Iterate over all child elements of the Placemark tag
        for child_elem in placemark:
            # Exclude geometry elements
            if child_elem.tag not in ['.//{http://www.opengis.net/kml/2.2}Point',
                                       './/{http://www.opengis.net/kml/2.2}LineString',
                                       './/{http://www.opengis.net/kml/2.2}Polygon']:
                # Add non-geometry tag values to properties
                if child_elem.text and child_elem.text.strip():  # Check if text exists and is not empty
                    feature_properties[child_elem.tag.split('}')[-1]] = child_elem.text.strip()

        # Get placemark geometry
        geom_elem = placemark.find('.//{http://www.opengis.net/kml/2.2}Point')
        if geom_elem is not None:
            coords_elem = geom_elem.find('.//{http://www.opengis.net/kml/2.2}coordinates')
            if coords_elem is not None:
                coords = coords_elem.text.strip().split(',')
                coordinates = [float(coords[0]), float(coords[1])]
                geometry = Point(geometry=coordinates, properties=feature_properties)
                features.append(geometry)

        geom_elem = placemark.find('.//{http://www.opengis.net/kml/2.2}LineString')
        if geom_elem is not None:
            coords_elem = geom_elem.find('.//{http://www.opengis.net/kml/2.2}coordinates')
            if coords_elem is not None:
                coordinates = [list(map(float, p.split(','))) for p in coords_elem.text.strip().split()]
                geometry = LineString(geometry=coordinates, properties=feature_properties)
                features.append(geometry)

        geom_elem = placemark.find('.//{http://www.opengis.net/kml/2.2}Polygon')
        if geom_elem is not None:
            outer_boundary = geom_elem.find('.//{http://www.opengis.net/kml/2.2}outerBoundaryIs')
            if outer_boundary is not None:
                coords_elem = outer_boundary.find('.//{http://www.opengis.net/kml/2.2}coordinates')
                if coords_elem is not None:
                    coordinates = [[list(map(float, p.split(','))) for p in coords_elem.text.strip().split()]]
                    geometry = Polygon(geometry=coordinates, properties=feature_properties)
                    features.append(geometry)

    geojson.add_features(features)
    return geojson



