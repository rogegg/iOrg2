from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class SignUpForm(ModelForm):
    email = forms.CharField(max_length=80, required=True)
    first_name = forms.CharField(max_length=80, required=True)
    last_name = forms.CharField(max_length=80, required=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }
