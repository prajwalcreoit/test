from django.shortcuts import render
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def register_patient(request):
    return render(request,'medic/register.html', {'form':RegisterForm})


def register_patient_validation(request):
    form = RegisterForm(request.POST, request.FILES)
    if form.is_valid():
        name = form.cleaned_data["name"]
        phone_no = form.cleaned_data["phone_no"]
        password = form.cleaned_data["password"]
        patient_obj = Patient(name=name, phone_no=phone_no, password=password)
        patient_obj.save()
        patient_obj.photo = request.FILES['picture']
        return render(request,'medic/login.html',{})
    else:
        return render(request,'medic/register.html',{'form':form})

