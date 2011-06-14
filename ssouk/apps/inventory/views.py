from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from apps.inventory.models import Item
from apps.inventory.forms import ItemForm


def list(request):
    """View which shows all the items presented in the ssouk.
    This is the gateway for the user, where she can select the map and 
    see all the items relevant to the query.
    
    For now report all the items, with the maps on top for the template.
    """
    latest_item_list = Item.objects.order_by('-expire_date')[:]
        
    return render_to_response('index.html', 
                              {'latest_item_list' : latest_item_list})
    
    
def user_items(request, username):
    """List all the items for the username
    Possible scenario:
    
    (i) user is on his own page: 
        - list the items
        - give the possibilities to add a new item
        - show the locations available
    (ii) user on another user page
        - list the items
        if friends:
            - show the precise location
        else:
            - show the neighborood
    (iii) not a logged user
        - list the items
        - show the city only
        
    P.S.: Location logic NOT YET IMPLEMENTED.
    """
    
    user = User.objects.filter(username=username)
    latest_item_list = Item.objects.filter(user__username=username
                                               ).order_by('-expire_date')[:]
    data = { 'latest_item_list' : latest_item_list,
            'username' : username}
    if user:    
        if request.user.is_authenticated():
            if username == request.user.username:
                data['same_user'] = True
                data['form'] =  add_item_form(request)
                
            else:
                # User logged in but not owner of the url.
                # Check if friends and then add location 
                # accordingly
                data['same_user'] = False
                
                
        else:
           # User is not logged in.
           # Only city.
           pass
            
        
        return render_to_response('inventory/user_list.html',
                                  data,
                                  RequestContext(request)
                                  )
        
    else:
        # User does not exist.
        return render_to_response('inventory/user_does_not_exist.html', 
                                  {'username' : username}, 
                                  )

@csrf_protect
def add_item_form(request):
    """Add an item to the inventory"""
    if request.method == 'POST': # If the form has been submitted...
        form = ItemForm(request.POST)
        
        if form.is_valid(): # All validation rules pass
            
            # Setting up the user directly from the post request. 
#            form.save(commit=False)
#            form.cleaned_data['user'] = request.user
            form.save()
            # Redirect after POST
#            return HttpResponseRedirect(reverse ('inventory.views.user_items', args=(request.user.username,))) 
    else:
        # A dynamically loaded form
        form = ItemForm(initial={'user' : request.user}) 

    return form