from django.urls import path
from . import views

app_name = "medic"
urlpatterns = [
    path('',views.register_patient, name='index'),
    path('register/', views.register_patient_validation, name='register_validation'),
    path('wardfillings/<int:pk>', views.WardFillings.as_view(), name='ward_fillings'),
    path('addmed/', views.add_medicine, name='add_medicine'),
    path('doctors/', views.ListDoctors.as_view(), name='list_doctors'),
    path('medicine/<int:pk>/', views.DetailMedicine.as_view(), name='detail_medicine'),
    path('medicine/', views.ListMedicine.as_view(), name='list_medicine'),
    path('editpat/<int:pk>/', views.EditPatient.as_view(), name='edit_patient'),
    path('delpat/<int:pk>/', views.DeletePatient.as_view(), name='delete_patient'),
]