from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def list(request, username, template='maps/locations.html'):
    data = {}
    if request.user.is_authenticated():
        if username == request.user.username:
                
                locations_obj = request.user.location_set.all()
                data['locations'] = locations_obj
                return render_to_response(template,
                              data,
                              context_instance=RequestContext(request)
                              )
        else:
            pass
            # User logged in but not owner of the url.
            # We should redirect her to her own locations.
            # TODO
            # HttpResponseRedirect()     