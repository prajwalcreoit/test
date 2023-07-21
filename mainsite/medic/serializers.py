from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = ['name', 'phone_no','photo','password']


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name','phone_no','password']