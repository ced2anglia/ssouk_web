from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('apps.inventory.views',
   url(r'^/(?P<username>\w+)/(?P<item_id>\d+)/$', 'item_detail', name='item_detail'),
   url(r'^/(?P<username>\w+)$', 'user_items', name='inventory-user-items'),
   url(r'^/(?P<username>\w+)/new', 'new', name='new-item'),
   url(r'^/$', 'list', name='inventory-list'),
   )