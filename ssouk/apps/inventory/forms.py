from django.db import models
from django.forms import ModelForm
from apps.inventory.models import Item
from uni_form.helpers import FormHelper, Submit, Reset


class ItemForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Item
        exclude = ('creation_date',
                   'user',
                   )
    
    @property
    def helper(self):
        # instantiate the form helper object
        helper = helpers.FormHelper()

        # add in some input controls (a.k.a. buttons)
        submit = helpers.Submit('submit','Submit')
        helper.add_input(submit)
        reset = helpers.Reset('reset','Reset')
        helper.add_input(reset)
        
        helper.form_action = 'new-item'
        helper.form_method = 'POST' # Only GET and POST are legal
        return helper
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(ItemForm, self).__init__(*args, **kwargs)
        