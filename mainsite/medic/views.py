from django.shortcuts import render
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

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
        patient_obj.save()

        return render(request,'medic/login.html',{})
    else:
        return render(request,'medic/register.html',{'form':form})

def add_medicine(request):
    if request.POST:
        med = Medicine()
        form = MedicineForm(request.POST, instance=med)
        if form.is_valid:
            form.save()
            return render(request, 'Medic/login.html', {})
        else:
            return render(request, 'Medic/login.html', {'form': form})
    else:
        return render(request, 'Medic/addmed.html', {'form':MedicineForm})


class list_doctors(View):
    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()
        return render(request,'Medic/listing.html',{'doctors': doctors})

class detail_medicine(DetailView):
    model = Medicine

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class list_medicine(ListView):
    model = Medicine

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context