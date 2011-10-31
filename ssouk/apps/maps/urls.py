from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('maps.views',
                       url(r'^(?P<username>\w+)/locations', 'list', name='locations_list'),
)