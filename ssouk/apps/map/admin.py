from django.contrib.gis import admin
from apps.map.models import Location

admin.site.register(Location, admin.GeoModelAdmin)