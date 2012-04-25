from tastypie.resources import ModelResource
from inventory.models import Item
from django.contrib.auth.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource = "user"
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        

class ItemResource(ModelResource):
    class Meta:
        queryset = Item.objects.all()
        resource = "item"
        