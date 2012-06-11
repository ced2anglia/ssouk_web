from django.db import models
from django.forms import ModelForm
from inventory.models import Item
from crispy_forms.helpers import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class ItemForm(ModelForm):
    
    class Meta:
        model = Item
        exclude = ('creation_date',
                   'user',
                   'selected'
                   )
    
    def __init__(self, user=None, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-new_item_form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'new_item'
        self.helper.form_class = 'form-horizontal'
        #self.helper.help_text_inline = True
        self.helper.layout = Layout(
                Field('name'),
                Field('university'),
                Field('category'),
                Field('description'),
                Field('location'),
                Field('expire_date'),
                Field('quantity'),
                Field('quantity_type'),
                Field('sell_individually'),
                Field('swappable'),
                Field('price', help_text_inline=True),
                #AppendedText('price', '&pound;'), #Needs investigation.
                Field('notes'),
                
                FormActions(
                           Reset('reset','Reset'),
                           Submit('submit', 'Add Item', css_class="btn-primary")
                           )
                               )
        self.user = user
        super(ItemForm, self).__init__(*args, **kwargs)
        