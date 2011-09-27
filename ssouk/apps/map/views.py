from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from apps.inventory.models import Item
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.gis.geos import Polygon
import simplejson
import datetime
from decimal import Decimal

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
            sw_x = float(request.GET.get('sw_x'))
            sw_y = float(request.GET.get('sw_y'))
            ne_x = float(request.GET.get('ne_x'))
            ne_y = float(request.GET.get('ne_y'))
        except:
            return HttpResponse(simplejson.dumps(dict(isOk=0, 
                                                      message='Did not get proper map boundaries')))
        
        
        poly = Polygon( [(sw_x,sw_y), (ne_x,sw_y), (ne_x,ne_y), (sw_x,ne_y), (sw_x,sw_y)] )
        searched_locations = Location.objects.filter(marker__within=poly)
        data = []
        for loc in searched_locations:
            items = loc.item_set.all()
            items_list = []
            for item in items:
                item_data = { 
                             'price' : str(item.price), 
                             'quantity' : str(item.quantity),
                             'date' : item.expire_date.isoformat(),
                             'pk' : item.pk,
                             'name' : str(item.name),
                             'username' : str(loc.user.username)
                            }
                items_list.append(item_data)
                                
            loc_dict = {
                        'lat' : loc.marker.get_y(), 
                        'lng' : loc.marker.get_x(),
                        'pk' : loc.pk,
                        'items' : items_list
                        }
            data.append(loc_dict)

        return HttpResponse(simplejson.dumps(data), 
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

    