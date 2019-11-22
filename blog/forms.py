from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
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

# class CustomFieldForm(PostFornm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('email', css_class='form-group col-md-6 mb-0'),
#                 Column('password', css_class='form-group col-md-6 mb-0'),
#                 css_class='form-row'
#             ),
#             'address_1',
#             'address_2',
#             Row(
#                 Column('city', css_class='form-group col-md-6 mb-0'),
#                 Column('state', css_class='form-group col-md-4 mb-0'),
#                 Column('zip_code', css_class='form-group col-md-2 mb-0'),
#                 css_class='form-row'
#             ),
#             CustomCheckbox('check_me_out'),
#             Submit('submit', 'Sign in')
#         )