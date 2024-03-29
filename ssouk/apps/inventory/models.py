 # -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from maps.models import Location
from category.models import Category 


from utils import expiring_date


# Each Item in the market
class Item(models.Model):
    QUANTITY_TYPE = (
                     ('Kg', 'Kilograms'),
                     ('L', 'Liter'),
                     ('item', 'Item')
                     )

    user = models.ForeignKey(User, related_name='item_creator_set')
    name =  models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    description = models.TextField()
    location = models.ForeignKey(Location)
    creation_date = models.DateTimeField(auto_now_add=True)
    available_from = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(default=expiring_date)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    quantity_type = models.CharField(max_length=4, choices=QUANTITY_TYPE)
    sell_individually = models.BooleanField()
    swappable = models.BooleanField()
    # Decimal to get the math right http://docs.python.org/library/decimal.html
    price = models.DecimalField(max_digits=20, decimal_places=2, help_text='£')
    notes = models.TextField(blank=True)
    selected = models.BooleanField()
    
    def __unicode__(self):
        return self.name

