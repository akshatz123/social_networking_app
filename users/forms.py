from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    dateofbirth = forms.DateField(label='Date of birth', widget=DateInput)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'dateofbirth']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    image = forms.ImageField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
