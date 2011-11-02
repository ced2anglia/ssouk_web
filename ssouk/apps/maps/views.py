from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.geos import Point

from utils import calculate_center, DEFAULT_CENTER_OBJ
from forms import LocationForm
from models import Location



import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
def list(request, template='maps/locations.html'):
    
    data = {}
    locations_obj = request.user.location_set.all()
    
    data['locations'] = locations_obj
    data['username'] = request.user.username
    data['center'] = calculate_center(locations_obj)
    
    return render_to_response(template,
                  data,
                  context_instance=RequestContext(request)
                  )

@csrf_protect
@login_required    
def add(request, form_class=LocationForm, template='maps/add_location.html'):
    center_obj = DEFAULT_CENTER_OBJ
    if request.method == 'POST': # If the form has been submitted...
        form = form_class(request.user, request.POST)
        if form.is_valid():
            
            location = form.save(commit=False)
            location.user = request.user
            location.save()
            request.user.message_set.create(
                    message=_("%(name)s has been saved.") %{'name': location.name})
            return HttpResponseRedirect(reverse('locations_list'))
        
    else:
        # A dynamically loaded form
        location = Location()
        location.marker = Point(center_obj['x'], center_obj['y'])
        form = form_class(initial={'user' : request.user,
                                   'marker' : location.marker})

    return render_to_response(template,
                              { "form": form, 
                                "center": center_obj
                               },
                              context_instance=RequestContext(request))

@login_required    
def edit(request, location_pk, form_class=LocationForm, template='maps/add_location.html'):
    
    location = Location.objects.get(pk=location_pk)
    center_obj = {"x" : location.marker.x, "y" : location.marker.y}
    if request.method == 'POST': # If the form has been submitted...
        form = form_class(request.user, request.POST)
        if form.is_valid():
            
            location = form.save(commit=False)
            location.user = request.user
            location.save()
            request.user.message_set.create(
                    message=_("%(name)s has been saved.") %{'name': location.name})
            return HttpResponseRedirect(reverse('locations_list'))
        
    else:
        # A dynamically loaded form
        form = form_class(initial={'user' : request.user, 
                                   'name' : location.name,
                                   'marker' : location.marker} )

    return render_to_response(template,
                              { "form": form,},
                              context_instance=RequestContext(request))
        
    
    