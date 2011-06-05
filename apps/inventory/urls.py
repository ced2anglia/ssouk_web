from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns("",
   (r'^/$', 'apps.inventory.views.list'),
   (r'^/(?P<username>\w+)$', 'apps.inventory.views.user_items'),
   )