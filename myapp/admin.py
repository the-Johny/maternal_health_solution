from django.contrib import admin
from .models import (
    # Patient Management Models
    Patient, EmergencyAlert,

    # Healthcare Provider Models
    Department, HealthcareProvider,

    # Appointment Management Models
    AppointmentType, Appointment,

    # Medical Records Models
    MedicalRecord, MedicalRecordAttachment,

    # Maternal Health Models
    PregnancyRecord, PregnancyConsultation, PostpartumSupport,
    Newborn, NewbornScreening, GeneticCounselling,

    # Virtual Consultation Models
    VirtualConsultation,

    # Analytics Models
    AnalyticsData
)

# Patient Management Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('_str_', 'gender', 'date_of_birth', 'blood_type', 'phone_number')
    list_filter = ('gender', 'blood_type')
    search_fields = ('user_first_name', 'userlast_name', 'user_email', 'phone_number')


@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = ('patient', 'alert_type', 'status', 'created_at', 'resolved_at')
    list_filter = ('alert_type', 'status')
    search_fields = ('patient_userfirst_name', 'patientuser_last_name', 'description')


# Healthcare Provider Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')


@admin.register(HealthcareProvider)
class HealthcareProviderAdmin(admin.ModelAdmin):
    list_display = ('_str_', 'specialization', 'license_number', 'department', 'experience_years')
    list_filter = ('specialization', 'department', 'is_available_for_virtual')
    search_fields = ('user_first_name', 'user_last_name', 'specialization', 'license_number')


# Appointment Management Admin
@admin.register(AppointmentType)
class AppointmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes')
    search_fields = ('name', 'description')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'appointment_type', 'scheduled_datetime', 'status', 'is_virtual')
    list_filter = ('status', 'appointment_type', 'is_virtual')
    search_fields = ('patient_userfirst_name', 'patientuser_last_name',
                     'provider_userfirst_name', 'provideruser_last_name', 'reason')
    date_hierarchy = 'scheduled_datetime'


# Medical Records Admin
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('patient_userfirst_name', 'patientuser_last_name',
                     'provider_userfirst_name', 'provideruser_last_name', 'diagnosis')
    date_hierarchy = 'created_at'


@admin.register(MedicalRecordAttachment)
class MedicalRecordAttachmentAdmin(admin.ModelAdmin):
    list_display = ('medical_record', 'description', 'created_at')
    search_fields = ('medical_record_patientuserfirst_name', 'medical_recordpatientuser_last_name', 'description')


# Maternal Health Admin
@admin.register(PregnancyRecord)
class PregnancyRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'due_date', 'is_high_risk')
    list_filter = ('is_high_risk',)
    search_fields = ('patient_userfirst_name', 'patientuser_last_name')

    def get_current_week(self, obj):
        return obj.current_week()

    get_current_week.short_description = 'Current Week'


@admin.register(PregnancyConsultation)
class PregnancyConsultationAdmin(admin.ModelAdmin):
    list_display = ('pregnancy_record', 'provider', 'week_of_pregnancy', 'status')
    list_filter = ('status', 'week_of_pregnancy')
    search_fields = ('pregnancy_record_patientuserfirst_name', 'pregnancy_recordpatientuser_last_name',
                     'provider_userfirst_name', 'provideruser_last_name')


@admin.register(PostpartumSupport)
class PostpartumSupportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'delivery_date', 'status')
    list_filter = ('status',)
    search_fields = ('patient_userfirst_name', 'patientuser_last_name',
                     'provider_userfirst_name', 'provideruser_last_name')
    date_hierarchy = 'delivery_date'


@admin.register(Newborn)
class NewbornAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patient', 'date_of_birth', 'gender', 'birth_weight')
    list_filter = ('gender',)
    search_fields = ('first_name', 'last_name', 'patient_userfirst_name', 'patientuser_last_name')
    date_hierarchy = 'date_of_birth'


@admin.register(NewbornScreening)
class NewbornScreeningAdmin(admin.ModelAdmin):
    list_display = ('newborn', 'provider', 'screening_type', 'screening_date', 'is_normal', 'follow_up_needed')
    list_filter = ('screening_type', 'is_normal', 'follow_up_needed')
    search_fields = ('newborn_first_name', 'newborn_last_name', 'screening_type')
    date_hierarchy = 'screening_date'


@admin.register(GeneticCounselling)
class GeneticCounsellingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'status', 'follow_up_needed')
    list_filter = ('status', 'follow_up_needed')
    search_fields = ('patient_userfirst_name', 'patientuser_last_name',
                     'provider_userfirst_name', 'provideruser_last_name', 'genetic_tests')


# Virtual Consultation Admin
@admin.register(VirtualConsultation)
class VirtualConsultationAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'meeting_platform', 'status')
    list_filter = ('meeting_platform', 'status')
    search_fields = ('appointment_patientuserfirst_name', 'appointmentpatientuser_last_name',
                     'appointment_provideruserfirst_name', 'appointmentprovideruser_last_name')


# Analytics Admin
@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ('data_type', 'date')
    list_filter = ('data_type',)
    date_hierarchy = 'date'