from datetime import datetime
from django.db import models
from django.contrib.auth.models import User 
from inventory.models import Item
from maps.models import Location


class Transaction(models.Model):

    buyer = models.ForeignKey(User, related_name='buyer')
    seller = models.ForeignKey(User, related_name='seller')
    item = models.ForeignKey(Item)
    location = models.ForeignKey(Location)
    meeting_time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    
    
    def __unicode__(self):
        return "From %s to %s for %s" %(self.buyer, self.seller, self.price)