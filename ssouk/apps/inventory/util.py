# All the util function for the inventory app


from datetime import datetime, timedelta
from django.contrib.gis.geos import Polygon
from maps.models import Location


def expiring_date(available_from=None, days=5):
    """Return the a future date adding `days` starting from the `available_from` date. 
       If not available_from is passed, datetime.now() is used as starting date.

       Params:
       -------
       available_from - starting date
       days - how many days should be added to the starting date.

       Return:
       expiring - the computed date

    """
    if available_from == None:
        available_from = datetime.now()
    expiring = available_from + timedelta(days=days)
    return expiring

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
