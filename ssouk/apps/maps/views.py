from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from inventory.models import Item
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.gis.geos import Polygon
import simplejson
import datetime
from decimal import Decimal

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)
 