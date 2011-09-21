from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from apps.inventory.models import Item
from apps.inventory.forms import ItemForm

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def list(request):
    """View which shows all the items presented in the ssouk.
    This is the gateway for the user, where she can select the map and 
    see all the items relevant to the query.
    
    For now report all the items, with the maps on top for the template.
    """
    items = Item.objects.order_by('-expire_date')[:]
        
    return render_to_response('index.html', 
                              {'items' : items},
                              context_instance=RequestContext(request))
    
    
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
    