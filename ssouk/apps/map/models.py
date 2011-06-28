from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """Class for the location which couple with the User.
    If you curious about the SRID read here: https://secure.wikimedia.org/wikipedia/en/wiki/SRID
    Of you want to know why 4326 and not 42 read here: 
        https://secure.wikimedia.org/wikipedia/en/wiki/WGS84
    """

    user = models.ForeignKey(User, related_name='location_creator_set')    
    name = models.CharField(max_length=32)
    marker = models.PointField(srid=4326) # the marker
    area = models.PolygonField(srid=4326, blank=True) #the area of delivery
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name 
    
    # Acces to maker:         self.marker.x, self.marker.y 
    # acess to area coords:   self.area.coords