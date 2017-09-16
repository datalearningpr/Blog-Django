
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from app.models import User

class BootstrapAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class RegisterForm(forms.Form):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

    confirm_password = forms.CharField(label=_("Confirm Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password Again'}))


    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and len(User.objects.filter(username=username))!=0:
            raise forms.ValidationError(_('username taken'))  
        return username


    def clean_confirm_password(self):

        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and password != confirm_password:
            raise forms.ValidationError(_('password confirm failed'))   
        return confirm_password


