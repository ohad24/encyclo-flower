import xml.etree.ElementTree as ET
from shapely.geometry import Point, Polygon
from functools import reduce
import operator
import math
from collections import defaultdict
import os


def etree_to_dict(t):
    """
    https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
    """
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(("@" + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def create_polygons_dict(kml_name):
    """
    parse the kml file and create a dictionary of polygons
    """
    kml_file_path = os.path.join(os.path.dirname(__file__), kml_name) + ".kml"
    tree = ET.parse(kml_file_path)
    root = etree_to_dict(tree.getroot())
    base_keys = "{http://www.opengis.net/kml/2.2}"
    placemarks = (
        root.get(base_keys + "kml")
        .get(base_keys + "Document")
        .get(base_keys + "Folder")
        .get(base_keys + "Placemark")
    )

    new_dict = {}

    for placemark in placemarks:
        location_name = placemark[base_keys + "name"]
        coordsTXT = (
            placemark.get(base_keys + "Polygon")
            .get(base_keys + "outerBoundaryIs")
            .get(base_keys + "LinearRing")
            .get(base_keys + "coordinates")
        )
        coords = []
        for j in coordsTXT.split(" "):
            j = j.split(",")
            coord = (float(j[0]), float(j[1]))
            coords.append(coord)
        center = tuple(
            map(
                operator.truediv,
                reduce(lambda x, y: map(operator.add, x, y), coords),
                [len(coords)] * 2,
            )
        )
        coords = sorted(
            coords,
            key=lambda coord: (
                -135
                - math.degrees(
                    math.atan2(*tuple(map(operator.sub, coord, center))[::-1])
                )
            )
            % 360,
        )
        polygon = Polygon(coords)
        new_dict[location_name] = polygon
    return new_dict


KML_dictionary = create_polygons_dict("All_Israel_Polygons2")


def find_point_location(coords):
    """
    check if coords in KML_dictionary and return location name
    if not exists
    """
    point = Point(coords)
    for loc in KML_dictionary:
        if point.within(KML_dictionary[loc]):
            return loc
    return False


# ! remove this function
if __name__ == "__main__":
    # p = (34.7, 32.0)
    latitude = 35.73356519465218
    longitude = 33.040111127472926
    coords = (latitude, longitude)
    ans = find_point_location(coords)
    print(ans)
