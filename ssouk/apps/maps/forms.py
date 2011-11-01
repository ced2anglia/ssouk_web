from django.forms import ModelForm
from uni_form.helpers import FormHelper
from uni_form.layout import Submit, Reset
from models import Location


from django import forms
from django.db import models
from django.utils.safestring import mark_safe

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 200

DEFAULT_LAT = 55.16
DEFAULT_LNG = 61.4

class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)

        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        if value is None:
            lat, lng = DEFAULT_LAT, DEFAULT_LNG
        else:
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
            lat, lng = float(a), float(b)

        js = '''
<script type="text/javascript">
//<![CDATA[
    var map_%(name)s;
    
    function savePosition_%(name)s(point)
    {
        var input = document.getElementById("id_%(name)s");
        input.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
        map_%(name)s.panTo(point);
    }
    
    function load_%(name)s() {
        var point = new google.maps.LatLng(%(lat)f, %(lng)f);

        var options = {
            zoom: 13,
            center: point,
            mapTypeId: google.maps.MapTypeId.ROADMAP
            // mapTypeControl: true,
            // navigationControl: true
        };
        
        map_%(name)s = new google.maps.Map(document.getElementById("map_%(name)s"), options);

        var marker = new google.maps.Marker({
                map: map_%(name)s,
                position: new google.maps.LatLng(%(lat)f, %(lng)f),
                draggable: true
        
        });
        google.maps.event.addListener(marker, 'dragend', function(mouseEvent) {
            savePosition_%(name)s(mouseEvent.latLng);
        });

        google.maps.event.addListener(map_%(name)s, 'click', function(mouseEvent){
            marker.setPosition(mouseEvent.latLng);
            savePosition_%(name)s(mouseEvent.latLng);
        });

    }
    
    $(document).ready(function(){
        load_%(name)s();
    });

//]]>
</script>
        ''' % dict(name=name, lat=lat, lng=lng)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat, lng), dict(id='id_%s' % name))
        html += '<div id="map_%s" style="width: %dpx; height: %dpx"></div>' % (name, self.map_width, self.map_height)

        return mark_safe(js + html)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
            'http://maps.google.com/maps/api/js?sensor=false',
        )

class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ('name',
                   'marker'
                   )
        widgets = {
            'marker': LocationWidget,
        }
 
    
    def __init__(self, user=None, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'saveLocation'
        self.helper.form_class = '' 
        self.helper.form_style = 'inline'
        self.helper.form_method = 'post'
        self.helper.form_action = 'add_location'
        self.helper.add_input(Reset('reset','Reset'))
        self.helper.add_input(Submit('submit','Submit'))
        self.user = user
        super(LocationForm, self).__init__(*args, **kwargs)