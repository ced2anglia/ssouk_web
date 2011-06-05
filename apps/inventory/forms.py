from django.db import models
from django.forms import ModelForm
from apps.inventory.models import Item

class ItemForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    class Meta:
        model = Item
        exclude = ('creation_date',
#                   'user',
                   )