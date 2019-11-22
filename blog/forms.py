from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Submit, Row
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from blog.fields import PostForm

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    date_of_birth = forms.DateTimeField(label='Date of birth', widget=DateInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2', 'first_name', 'last_name']


class PostForm(forms.Form):
    title= forms.CharField(max_length=500)
    content = forms.Textarea()
    image = forms.ImageField(required=False)
    video = forms.FileField(attrs={'accept':'video/*'})