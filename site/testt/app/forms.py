
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')
    tel = forms.CharField(max_length=15, required=True, help_text='Required')
    Nationalité = forms.CharField(max_length=50, required=True, help_text='Required')
    ville = forms.CharField(max_length=50, required=True, help_text='Required')
    Domicile = forms.CharField(max_length=50, required=True, help_text='Required')
    date_naissance = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    CIN = forms.CharField(max_length=15, required=True, help_text='Required')
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = (
            'last_name', 
            'first_name', 
            'email', 
            'tel', 
            'password1', 
            'password2', 
            'Nationalité', 
            'ville', 
            'Domicile', 
            'date_naissance', 
            'CIN', 
            'age'
        )
User = get_user_model()

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.',label='Email')