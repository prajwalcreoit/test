from django import forms
from django.core.validators import RegexValidator


class RegisterForm(forms.Form):
    name = forms.CharField(label="name", max_length=100)
    phone_no = forms.IntegerField(label="Ph_number", validators=[RegexValidator(regex=r'^[6-9]\d{9}$', message="Enter 10 Digit Mobile Number", code="10")])
    picture = forms.FileField(label='picture')
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput())