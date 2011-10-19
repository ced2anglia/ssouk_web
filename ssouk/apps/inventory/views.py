from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Polygon

from apps.map.models import Location
from apps.inventory.models import Item
from apps.inventory.forms import ItemForm
from util import search_items_within_poly

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

    
def user_items(request, username, template='inventory/user_list.html'):
    """List all the items for the username 
        - list the items
        - give the possibilities to add a new item
    """
    
    user = User.objects.filter(username=username)
    items = Item.objects.filter(user__username=username
                                               ).order_by('-expire_date')[:]
    data = {'items' : items,
            'username' : username,
            }
    if user:    
        if request.user.is_authenticated():
            if username == request.user.username:
                data['same_user'] = True
            else:
                # User logged in but not owner of the url.
                data['same_user'] = False
        return render_to_response('inventory/user_list.html',
                                  data,
                                  context_instance=RequestContext(request)
                                  )
    else:
        # User does not exist.
        return render_to_response('inventory/user_does_not_exist.html', 
                                  {'username' : username},
                                  context_instance=RequestContext(request) 
                                  )
@login_required
@csrf_protect
def new(request, username, form_class=ItemForm, template_name="inventory/new_item.html"):
    "Add a new item to the inventory."
    if request.method == 'POST': # If the form has been submitted...
        form = form_class(request.user, request.POST)
        if form.is_valid():
            logger.info('Saving the item in the db.')
            item = form.save(commit=False)
            item.user = request.user
            item.save()
#            request.user.message_set.create(
#                    message=_("%(name)s has been added to the SustainableSouk") %{'name': item.name})
            return HttpResponseRedirect(reverse('item_detail',
                        args=(request.user, item.pk,)))
        
    else:
        # A dynamically loaded form
        form = form_class(initial={'user' : request.user}) 
            
    return render_to_response(template_name,
                              { "form": form, 
                                "username": username,
                                },
                              context_instance=RequestContext(request))
            
def item_detail(request, username, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('inventory/item_detail.html', {'item': item})


#####
# Map interaction views

def list(request):
    """
    List the items within the default poly coords.    
    """
    
#    Bear in mind this is not synchronized with the Javascript map (map/static/js/map.js) 
#    at the beginning, so make sure those numbers and the centre of the map defined in the JS are the same.
    default_poly_coords = [(0.08636528015131262, 52.18927042707768), 
                           (0.15863471984857824, 52.18927042707768), 
                           (0.15863471984857824, 52.21083895608358), 
                           (0.08636528015131262, 52.21083895608358), 
                           (0.08636528015131262, 52.18927042707768)]
    
    
    items = search_items_within_poly(default_poly_coords)
            
    return render_to_response('index.html', 
                              {'items' : items},
                              context_instance=RequestContext(request))


@csrf_protect
def get_items_within_map(request):
    """ 
    Return a queryset of items within the map location.
    """
    
    if request.is_ajax():
        
        try:
            sw_x = float(request.GET.get('sw_x'))
            sw_y = float(request.GET.get('sw_y'))
            ne_x = float(request.GET.get('ne_x'))
            ne_y = float(request.GET.get('ne_y'))
            
        except:
            msg = 'Did not get proper map boundaries'
            return HttpResponse(simplejson.dumps(dict(message=msg)))
        # polygon for the search
        poly_coords = [(sw_x,sw_y), (ne_x,sw_y), (ne_x,ne_y), 
                       (sw_x,ne_y), (sw_x,sw_y)]
        
        print poly_coords
        items = search_items_within_poly(poly_coords)
        
        return render_to_response('inventory/list.snippet.html',
                              {'items' : items},
                              context_instance=RequestContext(request))    
    else: 
        return HttpResponseBadRequest()
    