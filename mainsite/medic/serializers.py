from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    medicines = serializers.PrimaryKeyRelatedField(many=True, queryset=Medicine.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'medicines']


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = ['name', 'phone_no','photo','password']


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name','phone_no','password']

class MedicineSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Medicine
        fields = ['name', 'company', 'owner']

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['name', 'price', 'number_of_beds']