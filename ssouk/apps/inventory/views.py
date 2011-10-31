from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Polygon

from maps.models import Location
from inventory.models import Item
from inventory.forms import ItemForm
from maps.utils import search_items_within_poly, calculate_center 
from maps.utils import DEFAULT_CENTER_OBJ, DEFAULT_POLY_COORDS

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
    locations = []
    for item in items:
        locations.append(item.location)
    
    
    center_obj = calculate_center(locations)
    data = {'items' : items,
            'username' : username,
            'center' : center_obj
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
        # Restricted to the location which belongs to the user
        form.fields['location'].queryset = Location.objects.filter(user=request.user.id)
         
            
    return render_to_response(template_name,
                              { "form": form, 
                                "username": username,
                                },
                              context_instance=RequestContext(request))
            
def item_detail(request, username, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render_to_response('inventory/item_detail.html', 
                              {'item': item},
                              context_instance=RequestContext(request)
                              )


#####
# Map interaction views

def list(request):
    """
    List the items within the default poly coords.    
    """
    # 

    
    items = search_items_within_poly(DEFAULT_POLY_COORDS)
            
    return render_to_response('inventory/general_customer_page.html', 
                              {'items' : items, 
                               'center' : DEFAULT_CENTER_OBJ},
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
    