from django.urls import path
from . import views

app_name = "medic"
urlpatterns = [
    path('',views.register_patient, name='index'),
    path('register/', views.register_patient_validation, name='register_validation'),
    path('addmed/', views.add_medicine, name='add_medicine'),
    path('listdr/', views.list_doctors.as_view(), name='list_doctors'),
    path('medicine/<int:pk>/', views.detail_medicine.as_view(), name='detail_medicine'),
    path('medicine/', views.list_medicine.as_view(), name='list_medicine')
]