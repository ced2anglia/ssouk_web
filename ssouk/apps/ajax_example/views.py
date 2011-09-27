from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
import simplejson
from django.http import HttpResponse

def index(request):
    
    return render_to_response('ajax_example/ajax_example_home.html',
                              context_instance=RequestContext(request))


def xhr_test(request):
    
    if request.is_ajax():
    
        try: 
            message = request.GET.get('message')
        except:
            message = "Data not supplied :("
        
    else:
        message = "Hello"
    return HttpResponse(simplejson.dumps(dict(message=message)), 
                        mimetype='application/json')