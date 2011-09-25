from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from apps.inventory.models import Item
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
import simplejson
from django.contrib.gis.geos import Polygon
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from apps.map.models import Location


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
    if request.is_ajax():
        
        try:
#            s = float(request.GET.get('s'))
#            w = float(request.GET.get('w'))
#            n = float(request.GET.get('n'))
#            e = float(request.GET.get('e'))
            # Swapping to deal with the Django Admin.
            # As soon we implement our stuff we drop this thing. (and we save lat and long.
            w = float(request.GET.get('s'))
            s = float(request.GET.get('w'))
            e = float(request.GET.get('n'))
            n = float(request.GET.get('e'))
        except:
            return HttpResponse(simplejson.dumps(dict(isOk=0, 
                                                      message='Did not get proper map boundaries')))
        
        print (type(s), s, w, n, e)
        poly = Polygon( [(s,w), (s,e), (n,e), (n,w), (s,w)] )
        print('Poly: %s' %poly)
        try:
            searched_locations = Location.objects.filter(marker__within=poly)
            print ('Searched location' + searched_locations)
            items = []
            for loc in searched_location:
                items.extend(loc.item_set.all())
            print items
        except:
            logger.error("I was unable to search!")
       
        
        return HttpResponse(simplejson.dumps(dict(isOk=1,
                                                  items=items)), 
                                                  mimetype='application/json')
    else: 
        
        return HttpResponseBadRequest()
    
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

    