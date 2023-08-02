from django.shortcuts import render
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django import forms
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.detail import SingleObjectMixin
from rest_framework import filters

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
        patient_obj.photo = form.cleaned_data['picture']
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


class ListDoctors(View):
    '''
    Listing Doctors with Builtin View
    '''

    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all()
        return render(request,'Medic/listing.html',{'doctors': doctors})


class DetailMedicine(DetailView):
    model = Medicine

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ListMedicine(ListView):
    model = Medicine
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class EditPatient(UpdateView):
    model = Patient
    fields = ['name','phone_no','photo','password']
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.id
        return context


class DeletePatient(DeleteView):
    model = Patient
    success_url = reverse_lazy('medic:index')


class WardFillings(SingleObjectMixin, ListView):
    paginate_by = 3
    template_name = 'Medic/ward_fillings.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Ward.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ward'] = self.object
        return context

    def get_queryset(self):
        return self.object.patient_set.all()


from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework import generics
from rest_framework import mixins
from django.contrib.auth.models import User
from .permissions import *
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['password']
    search_fields = ['name', 'phone_no']
    ordering_fields = ['name', 'date_admitted']
    ordering = ['name']

    @action(detail=True, methods=['get','post'], url_path='name_det')
    def name_detail(self, request, *args, **kwargs):
        patient = self.get_object()
        return Response({'name': patient.name})

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [BasicAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'phone_no']
    ordering_fields = ['name']

    @action(detail=True, methods=['get'], url_path='patients')
    def patients_details(self, request, *args, **kwargs):
        doctor = self.get_object()
        patients = doctor.patient_set.all()
        count = patients.count()
        return Response({'no_of_patients': count,
                         'patients': PatientSerializer(patients, many=True).data})

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name','price']

    @action(detail=True, methods=['get'], url_path='patients')
    def patients_details(self,request, *args, **kwargs):
        ward = self.get_object()
        patients = ward.patient_set.all()
        count = patients.count()
        return Response({'no_of_patients': count,
                         'patients': PatientSerializer(patients, many=True).data})


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def patient_list(request, format=None):

    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
@permission_classes((permissions.AllowAny,))
@renderer_classes([BrowsableAPIRenderer])
def patient_detail(request, pk, format=None):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DoctorList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DoctorInfo(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MedicineList(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    permission_classes = [IsOwnerOrReadOnly]


class MedicineInfo(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    lookup_fields = ['name', 'company']
    serializer_class = MedicineSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer