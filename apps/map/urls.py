from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^/$', 'apps.map.views.index'),
)