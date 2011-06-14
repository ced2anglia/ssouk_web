from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('apps.inventory.views',
   url(r'^/$', 'list', name='inventory-list'),
   url(r'^/(?P<username>\w+)$', 'user_items', name='inventory-user-items'),
   )