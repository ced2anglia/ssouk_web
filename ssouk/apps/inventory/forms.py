from django.db import models
from django.forms import ModelForm
from inventory.models import Item
from uni_form.helpers import FormHelper
from uni_form.layout import Submit, Reset


class ItemForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Item
        exclude = ('creation_date',
                   'user',
                   )
    
    def __init__(self, user=None, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-new_item_form'
        self.helper.form_class = 'blueForm'
        self.helper.form_style = 'inline'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_item'
        self.helper.add_input(Reset('reset','Reset'))
        self.helper.add_input(Submit('submit','Submit'))
        self.user = user
        super(ItemForm, self).__init__(*args, **kwargs)
        