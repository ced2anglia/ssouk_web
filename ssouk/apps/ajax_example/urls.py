from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('apps.ajax_example.views',
    url(r'^/xhr_test$','xhr_test'),
    url('^$', 'index'),
)