from django.contrib import admin
from .models import Patient, Doctor, Admin, Appointment, MedicalRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth', 'blood_group')
    search_fields = ('user__first_name', 'user__last_name', 'phone_number')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'is_verified')
    list_filter = ('specialization', 'is_verified')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_super_admin')
    list_filter = ('is_super_admin',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient__user__first_name', 'patient__user__last_name',
                    'doctor__user__first_name', 'doctor__user__last_name')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'diagnosis')
    list_filter = ('date',)
    search_fields = ('patient__user__first_name', 'patient__user__last_name',
                   'doctor__user__first_name', 'doctor__user__last_name',
                   'diagnosis')