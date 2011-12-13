from django.forms import ModelForm
from uni_form.helpers import FormHelper
from uni_form.layout import Submit, Reset
from models import Location

import floppyforms

class GMapPointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseGMapWidget):
    class Media:
        js = (
            'js/OpenLayers.js',
            )

class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ('name',
                   'marker'
                   )
        widgets = {
            'marker': GMapPointWidget,
        }
 
    
    def __init__(self, user=None, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'saveLocation'
        self.helper.form_class = '' 
        self.helper.form_method = 'post'
        self.helper.add_input(Reset('reset','Reset'))
        self.helper.add_input(Submit('submit','Submit'))
        self.user = user
        super(LocationForm, self).__init__(*args, **kwargs)

class AddLocationForm(LocationForm):
    def __init__(self, *args, **kwargs):
        super(AddLocationForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'add_location'
    
        
    
class EditLocationForm(LocationForm):
    def __init__(self, *args, **kwargs):
        super(EditLocationForm, self).__init__(*args, **kwargs)
        self.helper.form_action = '' #Got it from the location instance
        
        
    
    
    
    
    