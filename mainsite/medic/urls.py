from django.urls import path
from . import views

app_name = "medic"
urlpatterns = [
    path('',views.RegisterPatient,name='index'),
    path('register/',views.RegisterPatient_validation,name='register_validation')
]