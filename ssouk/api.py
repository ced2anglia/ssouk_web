from tastypie.resources import ModelResource
from inventory.models import Item
from django.contrib.auth.models import User
from maps.models import Location
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource = "user"
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        

class ItemResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    
    class Meta:
        queryset = Item.objects.all()
        resource = "item"
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'name': ALL,
            'expire_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()

class LocationResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    
    class Meta:
        queryset = Location.objects.all()
        resource = "location"
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'name': ALL,
            'marker': ['exact', 'lt', 'lte', 'gte', 'gt', 'within'],
        }
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()        