from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.inventory.models import Item

def index(request):
    
    items = Item.objects.order_by('name')
        
    return render_to_response('map/map.html', 
                              { 'items' : items },
                              context_instance=RequestContext(request))
    
def get_markers_on_map(request, map_bounderies):
    """ Return the location of the items in the request
    this should answer to an an AJAX request coming to an URL 
    with the map coords.
    """
    # check if is AJAX
    lat, long = map_bounderies
    # search for the bounderies on the db
    
    # return the selected Item
    

