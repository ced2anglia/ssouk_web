from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('maps.views',
                       url(r'^$', 'list', name='locations_list'),
)