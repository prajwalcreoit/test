from django.db import models
from django.utils import timezone

# Create your models here.

def user_directory_path(instance, filename):
    return "pateint/{0}/{1}".format(instance.id, filename)

class Receptionist(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.BigIntegerField(default=None,null=True,blank=True)
    password = models.CharField(max_length=100,default='password')
    def __str__(self):
        return self.name

class Ward(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=1000)
    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    phone_no = models.BigIntegerField(default=None,null=True,blank=True)
    password = models.CharField(max_length=100,default='password')

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=200,default="Govt")

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_admitted = models.DateTimeField(default=timezone.now())
    phone_no = models.BigIntegerField(default=None,null=True,blank=True)
    photo = models.FileField(upload_to=user_directory_path,default=None,null=True)
    prescribed = models.ManyToManyField(Medicine)
    treated_by = models.ManyToManyField(Doctor)
    ward = models.ForeignKey(Ward,on_delete=models.PROTECT,null=True,default=None)
    password = models.CharField(max_length=100, default='password')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

