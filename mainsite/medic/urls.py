from django.urls import path
from . import views
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'doctors', views.DoctorViewSet)

app_name = "medic"
urlpatterns = [
    path('',views.register_patient, name='index'),

    path('apis/', include(router.urls)),
    path('apis/userlis/',views.UserList.as_view()),
    path('apis/userinfo/<int:pk>/', views.UserDetail.as_view()),
    path('apis/patlis/', views.patient_list),
    path('apis/patinfo/<int:pk>', views.patient_detail),
    path('apis/medlis/', views.MedicineList.as_view(), name='medicine_list'),
    path('apis/medinfo/<str:name>/<str:company>', views.MedicineInfo.as_view(), name='medicine_info'),
    path('apis/doclis/', views.DoctorList.as_view()),
    path('apis/docinfo/<int:pk>', views.DoctorInfo.as_view()),

    path('register/', views.register_patient_validation, name='register_validation'),
    path('wardfillings/<int:pk>', views.WardFillings.as_view(), name='ward_fillings'),
    path('addmed/', views.add_medicine, name='add_medicine'),
    path('doctors/', views.ListDoctors.as_view(), name='list_doctors'),
    path('medicine/', views.ListMedicine.as_view(), name='list_medicine'),
    path('medicine/<int:pk>/', views.DetailMedicine.as_view(), name='detail_medicine'),
    path('editpat/<int:pk>/', views.EditPatient.as_view(), name='edit_patient'),
    path('delpat/<int:pk>/', views.DeletePatient.as_view(), name='delete_patient'),
]
