from django import forms
from .models import Delivery

class DeliveryForm(forms.ModelForm):

    class Meta:
        model = Delivery
        field = ('supplier_name', 'author', 'price', 'delivery_time', 'status')