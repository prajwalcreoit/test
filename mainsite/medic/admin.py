from django.contrib import admin
from .models import *

# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id','is_active',"name", "phone_no", "ward"]

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id',"name", "phone_no"]

class WardAdmin(admin.ModelAdmin):
    list_display = ['id',"name", "price"]

class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ['id',"name", "phone_no"]

class MedicineAdmin(admin.ModelAdmin):
    list_display = ['id',"name", "company"]


admin.site.register(Patient,PatientAdmin)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Ward,WardAdmin)
admin.site.register(Receptionist,ReceptionistAdmin)
admin.site.register(Medicine,MedicineAdmin)
