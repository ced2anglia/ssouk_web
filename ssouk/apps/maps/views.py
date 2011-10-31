from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse

from utils import calculate_center


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def list(request, template='maps/locations.html'):
    data = {}
    if request.user.is_authenticated():
        
        locations_obj = request.user.location_set.all()
        data['locations'] = locations_obj
        data['username'] = request.user.username
        data['center'] = calculate_center(locations_obj)
        return render_to_response(template,
                      data,
                      context_instance=RequestContext(request)
                      )
    else:
        return(HttpResponseRedirect(reverse('general_customer')))