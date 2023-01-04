from django import forms
from .models import ShopAbout, ContactUs

class ShopAbout(forms.ModelForm):

    class Meta:
        model = ShopAbout
        fields = ('name', 'description')

class ContactUs(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ('title', 'shop', 'address', 'email', 'email')