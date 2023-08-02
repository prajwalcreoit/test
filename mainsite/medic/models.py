from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.urls import reverse
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

def user_directory_path(instance, filename):
    return "pateint/{0}/{1}".format(instance.id, filename)


class Receptionist(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.BigIntegerField(default=None, null=True, blank=True, validators=[RegexValidator(regex=r'^[6-9]\d{9}$', message="Enter 10 Digit Mobile Number", code="10")])
    password = models.CharField(max_length=100, default='password')
    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=1000)
    number_of_beds = models.IntegerField(default=100)
    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.BigIntegerField(default=None, null=True, blank=True, validators=[RegexValidator(regex=r'^[6-9]\d{9}$', message="Enter 10 Digit Mobile Number", code="10")])
    password = models.CharField(max_length=100, default='password')

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=200, default="Govt")
    owner = models.ForeignKey('auth.User', related_name='medicines', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_admitted = models.DateTimeField(default=timezone.now())
    phone_no = models.BigIntegerField(default=None, null=True, blank=True, validators=[RegexValidator(regex=r'^[6-9]\d{9}$', message="Enter 10 digit phone number", code='10')])
    photo = models.FileField(upload_to=user_directory_path, default=None, null=True)
    prescribed = models.ManyToManyField(Medicine)
    treated_by = models.ManyToManyField(Doctor)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, default=None)
    password = models.CharField(max_length=100, default='password')
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("medic:index")

    def __str__(self):
        return self.name

class MedicineForm(ModelForm):
    class Meta:
        model = Medicine
        fields = ['name','company']