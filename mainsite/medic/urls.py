from django.urls import path
from . import views

app_name = "medic"
urlpatterns = [
    path('',views.register_patient,name='index'),
    path('register/',views.register_patient_validation,name='register_validation')
]