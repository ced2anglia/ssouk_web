# Utils for maps.

from django.contrib.gis.geos import Polygon
from models import Location



DEFAULT_POLY_COORDS = [(0.08636528015131262, 52.18927042707768), 
                       (0.15863471984857824, 52.18927042707768), 
                       (0.15863471984857824, 52.21083895608358), 
                       (0.08636528015131262, 52.21083895608358), 
                       (0.08636528015131262, 52.18927042707768)]
DEFAULT_CENTER_OBJ = {"x" : 0.12249999999994543, "y" : 52.20005469158063 }


def search_items_within_poly(poly_coords):
    """Search the items which location is contained within the poly and return 
    them as a list of queryset.
    
    Params:
    -------
    poly_coords - Must be a set of coords (long, lat) where the last one should 
                  be equal to the first point. 
                  Example: default_poly_coords = [(0.08, 52.19), (0.15, 52.19), 
                                                  (0.15, 52.21), (0.08, 52.21),
                                                  (0.08, 52.19)] 
    """
    
    poly = Polygon(poly_coords)
    searched_locations = Location.objects.filter(marker__within=poly)
    items = [] 
    # For each location we collect the items and add them to the list.
    for loc in searched_locations: 
        items.extend(loc.item_set.all())
    
    return items


def calculate_center(markers):
    "Calculate the center of different locations"
    if len(markers) == 1:
        loc = markers[0]
        return (marker.x, marker.y)
    elif len(markers) > 2:
        markers_x = []
        markers_y = []
        for marker in markers:
            markers_x.append(marker.x)
            markers_y.append(marker.y)
            
        center_x = _calc_middle_point(markers_x)
        center_y = _calc_middle_point(markers_y)
        center = {"x" : center_x, "y" : center_y}
        return center
    else:
        return DEFAULT_CENTER_OBJ


def _calc_middle_point(values):
    
    minimum = min(values)
    maximum = max(values)
    delta = maximum - minimum
    middle_point = minimum + delta/2
    return middle_point
        
        
         