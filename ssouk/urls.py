from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ssouk_web.views.home', name='home'),
    # url(r'^ssouk_web/', include('ssouk_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url('^$', direct_to_template, {'template': 'home.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inventory', include("inventory.urls")),
    url(r'^maps', include("maps.urls")),
    url(r'^waypoints', include('waypoints.urls')),
    #url(r'^ajax_example', include('ajax_example.urls')),
)


