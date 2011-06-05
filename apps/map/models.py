from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):

    user = models.ForeignKey(User, related_name='location_creator_set')
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()