from datetime import datetime
from django.db import models
from django.contrib.auth.models import User 
from apps.inventory import Item


class Transaction(models.Model):

    buyer = models.ForeignKey(User, related_name='item_creator_set')
    seller = models.ForeignKey(Item.user)
    item = models.ForeignKey(Item)
    location = models.ForeignKey(Item.location)
    
    meeting_time = models.DateTimeField(auto_now_add=True)
    price = models.ForeignKey(Item.price)
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.pk, self.item__name