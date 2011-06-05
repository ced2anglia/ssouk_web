from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


from util import expiring_date



# Each Item in the market
class Item(models.Model):
    user = models.ForeignKey(User, related_name='item_creator_set')
    name =  models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    available_from = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(default=expiring_date)
    quantity = models.CharField(max_length=50)
    # Decimal to get the math right http://docs.python.org/library/decimal.html
    price = models.DecimalField(max_digits=20, decimal_places=2) 
    description = models.TextField()
    #image = models.ImageField(upload_to='item', blank=True)
    
    def __unicode__(self):
        return self.name

