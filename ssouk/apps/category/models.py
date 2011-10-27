from django.db import models

CATEGORY_TYPE = (
                 ('V', 'Vegetables',
                  'F', 'Fruits'
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
    image = models.ImageField(blank=True, upload_to='category', height_field=16, width_field=16)
    
    def __unicode__(self):
        return self.name