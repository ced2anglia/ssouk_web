from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.map.views',
    url(r'^/$', 'index', name ="map-index"),
    url(r'/get_markers_on_map', 'get_markers_on_map', name='marker_search')
)