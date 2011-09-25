from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from apps.inventory.models import Item
from django.http import HttpResponse, HttpResponseRedirect
import simplejson
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    
    items = Item.objects.order_by('name')
    
    return render_to_response('map/map.html', 
                              { 'items' : items },
                              context_instance=RequestContext(request))
@csrf_protect
def get_markers_on_map(request):
    """ Return the location of the items in the request
    this should answer to an an AJAX request coming to an URL 
    with the map coords.
    """
    logger.info('Inside the markers view.')
    
    try:
        bounds = request.GET.get('map_bounds')
        w,s,e,n = b[0][0],b[0][1],b[1][0],b[1][1] #swapping 'cause the django admin
                                                  #saves as log/lat instead, google 
                                                  #return lat/log. This has to change.
        poly = Polygon( [(s,w), (s,e), (n,e), (n,w), (s,w)] )
        searched_locations = Location.objects.filter(marker__within=poly)
        items = []
        for loc in searched_location:
            items.extend(loc.item_set.all())
        
    except:
        return HttpResponse(simplejson.dumps(dict(isOk=0, 
                                                  message='Did not get proper \
                                                  map boundaries')))
    
    return HttpResponse(simplejson.dumps(dict(
                                              isOk=1,
                                              items=items)), 
                                              mimetype='application/json')
def xhr_test(request):
    
    if request.is_ajax():
        
        try: 
            message = request.GET.get('message')
        except:
            message = "Data not supplied :("
        
    else:
        message = "Hello"
    return HttpResponse(simplejson.dumps(dict(message=message)), 
                        mimetype='application/json')

    