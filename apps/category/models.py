from django.db import models

CATEGORY_TYPE = (
                 ('V', 'Vegetables',
                  'F', 'Fruit'
                  'M', 'Meat'
                  'Fi' 'Fish',
                  'D', 'Dairy',
                  'B', 'Beverages',
                  'G', 'Garden',
                  'O', 'Other' 
                  )
                 )
# Create your models here.
class Category(models.Model):
    name =  models.CharField(max_length=10)
    image = Model.ImageField(blank=True)