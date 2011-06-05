from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.map.views',
    url(r'^/$', 'index'),
)