from django.contrib.auth.models import User
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import models


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):
    dateofbirth = forms.DateField(label='Date of birth', widget=DateInput)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'dateofbirth',
            'email'
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    image = forms.ImageField()

    class Meta:
        model = User
        fields = [
            'image',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
