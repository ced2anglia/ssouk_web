from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('inventory.views',
   url(r'^get_items_within_map', 'get_items_within_map', name='get_items_within_map'),
   url(r'^(?P<username>\w+)/(?P<item_id>\d+)/$', 'item_detail', name='item_detail'),
   url(r'^(?P<username>\w+)$', 'user_items', name='inventory_user_items'),
   url(r'^(?P<username>\w+)/new', 'new', name='new_item'),
   url(r'^$', 'list', name='inventory_list'),
   )