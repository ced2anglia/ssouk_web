from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ssouk_web.views.home', name='home'),
    # url(r'^ssouk_web/', include('ssouk_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
    
    (r'^admin/', include(admin.site.urls)),
    
    
    (r'^inventory', include("apps.inventory.urls")),
    (r'^map', include("apps.map.urls")),
    (r'^waypoints', include('apps.waypoints.urls')),
    (r'^ajax_example', include('apps.ajax_example.urls')),
)


