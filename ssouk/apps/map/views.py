from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.inventory.models import Item

def index(request):
    
    items = Item.objects.order_by('name')
        
    return render_to_response('map/map.html', 
                              { 'items' : items },
                              context_instance=RequestContext(request))
    

