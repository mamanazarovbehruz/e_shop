from django import forms
from .models import User
from django.contrib.auth import authenticate


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length=128)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password1')
        

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)
    
    def user_auth(self):
        user = authenticate(**self.cleaned_data)
        if user:
            return user
        return None

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('date_joined', 'last_login', 'groups', 'user_permissions')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'about', 'user_currency', 'address1', 'phonenumber', 'email')

class UserCurrencyForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('user_currency',)

class UserCardChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('card_number', 'card_date', 'currency')

class UserChangePassword(forms.Form):
    password = forms.CharField(max_length=128)
    password1 = forms.CharField(max_length=128)
    password2 = forms.CharField(max_length=128)

class UserAddressForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('country', 'city', 'region', 'zip_code', 'address1')

class UserRoleForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('role',)

