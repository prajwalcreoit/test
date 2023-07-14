from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label="name", max_length=100)
    phone_no = forms.IntegerField(label="Ph_number")
    picture = forms.FileField(label='picture')
    password = forms.CharField(label='password',max_length=100,widget=forms.PasswordInput())