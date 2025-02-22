from django import forms
from django.forms import ModelForm, DateInput, Textarea, Select, DateTimeInput
from django.forms.widgets import FileInput
from django.contrib.auth.models import User
from .models import (
    Patient, EmergencyAlert, Department, HealthcareProvider,
    AppointmentType, Appointment, MedicalRecord, MedicalRecordAttachment,
    PregnancyRecord, PregnancyConsultation, PostpartumSupport,
    Newborn, NewbornScreening, GeneticCounselling,
    VirtualConsultation
)


# Patient form
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'gender', 'phone_number', 'address', 'emergency_contact_name',
                  'emergency_contact_phone', 'blood_type', 'allergies', 'chronic_conditions',
                  'insurance_provider', 'insurance_policy_number']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'allergies': Textarea(attrs={'rows': 3}),
            'chronic_conditions': Textarea(attrs={'rows': 3}),
        }


# Emergency Alert form
class EmergencyAlertForm(ModelForm):
    class Meta:
        model = EmergencyAlert
        fields = ['alert_type', 'description', 'location']
        widgets = {
            'description': Textarea(attrs={'rows': 4, 'placeholder': 'Please describe the emergency situation...'}),
            'location': Textarea(attrs={'rows': 2, 'placeholder': 'Where is the emergency taking place?'})
        }


# Healthcare Provider form
class ProviderForm(ModelForm):
    class Meta:
        model = HealthcareProvider
        fields = ['specialization', 'department', 'license_number', 'bio', 'office_location',
                  'phone_number', 'available_for_virtual_consultation']
        widgets = {
            'bio': Textarea(attrs={'rows': 4}),
            'office_location': Textarea(attrs={'rows': 2}),
        }


# Appointment form
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['provider', 'appointment_type', 'scheduled_datetime', 'reason', 'is_virtual', 'notes']
        widgets = {
            'scheduled_datetime': DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': Textarea(attrs={'rows': 3}),
            'notes': Textarea(attrs={'rows': 3}),
        }

    def _init_(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super(AppointmentForm, self)._init_(*args, **kwargs)

        # If this is a patient form, we need to filter available providers
        if patient:
            # Logic to filter providers if needed
            pass


# Medical Record form
class MedicalRecordForm(ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'symptoms', 'treatment_plan', 'medications',
                  'notes', 'followup_required', 'followup_date']
        widgets = {
            'diagnosis': Textarea(attrs={'rows': 2}),
            'symptoms': Textarea(attrs={'rows': 3}),
            'treatment_plan': Textarea(attrs={'rows': 4}),
            'medications': Textarea(attrs={'rows': 3}),
            'notes': Textarea(attrs={'rows': 4}),
            'followup_date': DateInput(attrs={'type': 'date'}),
        }


# Medical Record Attachment form (if needed)
class MedicalRecordAttachmentForm(ModelForm):
    class Meta:
        model = MedicalRecordAttachment
        fields = ['file', 'description']
        widgets = {
            'file': FileInput(),
            'description': Textarea(attrs={'rows': 2}),
        }


# Pregnancy Record form
class PregnancyRecordForm(ModelForm):
    class Meta:
        model = PregnancyRecord
        fields = ['estimated_conception_date', 'due_date', 'blood_type', 'pregnancy_risk_level',
                  'previous_pregnancies', 'pre_pregnancy_weight', 'pre_existing_conditions', 'notes']
        widgets = {
            'estimated_conception_date': DateInput(attrs={'type': 'date'}),
            'due_date': DateInput(attrs={'type': 'date'}),
            'pre_existing_conditions': Textarea(attrs={'rows': 3}),
            'notes': Textarea(attrs={'rows': 4}),
        }


# Pregnancy Consultation form
class PregnancyConsultationForm(ModelForm):
    class Meta:
        model = PregnancyConsultation
        fields = ['gestational_age', 'weight', 'blood_pressure', 'fetal_heart_rate',
                  'fundal_height', 'symptoms', 'notes', 'next_appointment']
        widgets = {
            'symptoms': Textarea(attrs={'rows': 3}),
            'notes': Textarea(attrs={'rows': 4}),
            'next_appointment': DateInput(attrs={'type': 'date'}),
        }


# Postpartum Support form
class PostpartumSupportForm(ModelForm):
    class Meta:
        model = PostpartumSupport
        fields = ['mother_condition', 'emotional_state', 'lactation_status',
                  'complications', 'recommendations', 'next_appointment']
        widgets = {
            'mother_condition': Textarea(attrs={'rows': 3}),
            'emotional_state': Textarea(attrs={'rows': 3}),
            'lactation_status': Textarea(attrs={'rows': 2}),
            'complications': Textarea(attrs={'rows': 3}),
            'recommendations': Textarea(attrs={'rows': 4}),
            'next_appointment': DateInput(attrs={'type': 'date'}),
        }


# Newborn form
class NewbornForm(ModelForm):
    class Meta:
        model = Newborn
        fields = ['first_name', 'last_name', 'date_of_birth', 'time_of_birth',
                  'gender', 'weight', 'height', 'head_circumference', 'delivery_type',
                  'complications', 'apgar_score', 'blood_type', 'notes']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'time_of_birth': forms.TimeInput(attrs={'type': 'time'}),
            'complications': Textarea(attrs={'rows': 3}),
            'notes': Textarea(attrs={'rows': 4}),
        }


# Newborn Screening form
class NewbornScreeningForm(ModelForm):
    class Meta:
        model = NewbornScreening
        fields = ['screening_type', 'screening_date', 'result', 'follow_up_needed',
                  'follow_up_date', 'notes']
        widgets = {
            'screening_date': DateInput(attrs={'type': 'date'}),
            'result': Textarea(attrs={'rows': 3}),
            'follow_up_date': DateInput(attrs={'type': 'date'}),
            'notes': Textarea(attrs={'rows': 4}),
        }


# Genetic Counselling form
class GeneticCounsellingForm(ModelForm):
    class Meta:
        model = GeneticCounselling
        fields = ['reason_for_referral', 'family_history', 'genetic_tests_recommended',
                  'test_results', 'counselling_notes', 'follow_up_plan']
        widgets = {
            'reason_for_referral': Textarea(attrs={'rows': 3}),
            'family_history': Textarea(attrs={'rows': 4}),
            'genetic_tests_recommended': Textarea(attrs={'rows': 3}),
            'test_results': Textarea(attrs={'rows': 3}),
            'counselling_notes': Textarea(attrs={'rows': 4}),
            'follow_up_plan': Textarea(attrs={'rows': 3}),
        }


# Virtual Consultation form
class VirtualConsultationForm(ModelForm):
    class Meta:
        model = VirtualConsultation
        fields = ['meeting_link', 'platform', 'meeting_id', 'passcode', 'instructions']
        widgets = {
            'meeting_link': forms.URLInput(attrs={'placeholder': 'Enter full meeting URL'}),
            'instructions': Textarea(
                attrs={'rows': 4, 'placeholder': 'Enter any special instructions for joining the meeting...'}),
        }