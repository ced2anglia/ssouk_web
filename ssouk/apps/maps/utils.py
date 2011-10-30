# Utils for maps.

from django.contrib.gis.geos import Polygon
from models import Location

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