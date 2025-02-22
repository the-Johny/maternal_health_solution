from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Base model with created and updated timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseStatusModel(BaseModel):
    """Base model with status field"""
    STATUS_CHOICES = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        abstract = True


# Patient Management Models
class Patient(BaseModel):
    """Model for storing patient details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ))
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    blood_type = models.CharField(max_length=5, choices=(
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ), null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    chronic_conditions = models.TextField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)

    def _str_(self):
        return f"{self.user.first_name} {self.user.last_name}"


class EmergencyAlert(BaseStatusModel):
    """Model for tracking emergency alerts raised by patients"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_alerts')
    alert_type = models.CharField(max_length=50, choices=(
        ('medical', _('Medical Emergency')),
        ('maternal', _('Maternal Emergency')),
        ('other', _('Other Emergency')),
    ))
    description = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.patient} - {self.alert_type} - {self.status}"


# Healthcare Provider Models
class Department(BaseModel):
    """Model for hospital/clinic departments"""
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def _str_(self):
        return self.name


class HealthcareProvider(BaseModel):
    """Model for healthcare providers/doctors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='providers')
    qualification = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=15)
    availability = models.JSONField(default=dict)  # Store availability schedule as JSON
    is_available_for_virtual = models.BooleanField(default=True)

    def _str_(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"


# Appointment Management Models
class AppointmentType(BaseModel):
    """Model for different types of appointments"""
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)

    def _str_(self):
        return self.name


class Appointment(BaseStatusModel):
    """Model for tracking appointments between patients and providers"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.ForeignKey(AppointmentType, on_delete=models.SET_NULL, null=True)
    scheduled_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reason = models.TextField()
    is_virtual = models.BooleanField(default=False)
    meeting_link = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.patient} - {self.provider} - {self.scheduled_datetime.strftime('%Y-%m-%d %H:%M')}"


# Medical Records Models
class MedicalRecord(BaseModel):
    """Model for storing patient medical records"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='medical_records')
    diagnosis = models.TextField()
    prescription = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.patient} - {self.created_at.strftime('%Y-%m-%d')}"


class MedicalRecordAttachment(BaseModel):
    """Model for storing attachments related to medical records"""
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='medical_records/')
    description = models.CharField(max_length=255, null=True, blank=True)

    def _str_(self):
        return f"Attachment for {self.medical_record}"


# Maternal Health Models
class PregnancyRecord(BaseModel):
    """Model for tracking pregnancy details"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='pregnancy_records')
    due_date = models.DateField()
    start_date = models.DateField()  # Estimated conception date
    is_high_risk = models.BooleanField(default=False)
    risk_factors = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.patient} - Due: {self.due_date}"

    def current_week(self):
        """Calculate current week of pregnancy"""
        import datetime
        today = datetime.date.today()
        if today > self.due_date:
            return "Post-delivery"
        return (today - self.start_date).days // 7 + 1


class PregnancyConsultation(BaseStatusModel):
    """Model for tracking pregnancy consultations"""
    pregnancy_record = models.ForeignKey(PregnancyRecord, on_delete=models.CASCADE, related_name='consultations')
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE, related_name='pregnancy_consultations')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    week_of_pregnancy = models.PositiveIntegerField()
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in kg
    fetal_heart_rate = models.PositiveIntegerField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.pregnancy_record.patient} - Week {self.week_of_pregnancy}"


class PostpartumSupport(BaseStatusModel):
    """Model for tracking postpartum support sessions"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='postpartum_support')
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE, related_name='postpartum_support')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_date = models.DateField()
    physical_recovery = models.TextField(null=True, blank=True)
    mental_health = models.TextField(null=True, blank=True)
    lactation_support = models.TextField(null=True, blank=True)
    nutritional_guidance = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.patient} - {self.delivery_date}"


class Newborn(BaseModel):
    """Model for newborn details"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='newborns')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=(
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ))
    birth_weight = models.DecimalField(max_digits=4, decimal_places=2)  # in kg
    birth_length = models.DecimalField(max_digits=4, decimal_places=1)  # in cm
    apgar_score = models.CharField(max_length=10, null=True, blank=True)
    complications = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.first_name} {self.last_name} ({self.date_of_birth})"


class NewbornScreening(BaseModel):
    """Model for tracking newborn screening results"""
    newborn = models.ForeignKey(Newborn, on_delete=models.CASCADE, related_name='screenings')
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE, related_name='newborn_screenings')
    screening_date = models.DateField()
    screening_type = models.CharField(max_length=100)
    results = models.TextField()
    is_normal = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)
    follow_up_needed = models.BooleanField(default=False)
    follow_up_notes = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.newborn} - {self.screening_type}"


class GeneticCounselling(BaseStatusModel):
    """Model for tracking genetic counselling sessions"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='genetic_counselling')
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE, related_name='genetic_counselling')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    family_history = models.TextField()
    genetic_tests = models.TextField(null=True, blank=True)
    test_results = models.TextField(null=True, blank=True)
    recommendations = models.TextField(null=True, blank=True)
    follow_up_needed = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.patient} - {self.created_at.strftime('%Y-%m-%d')}"


# Virtual Consultation Models
class VirtualConsultation(BaseStatusModel):
    """Model for tracking virtual consultations"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='virtual_consultation')
    meeting_platform = models.CharField(max_length=50, choices=(
        ('zoom', _('Zoom')),
        ('teams', _('Microsoft Teams')),
        ('google_meet', _('Google Meet')),
        ('other', _('Other')),
    ))
    meeting_id = models.CharField(max_length=100, null=True, blank=True)
    meeting_password = models.CharField(max_length=50, null=True, blank=True)
    recording_url = models.URLField(null=True, blank=True)
    technical_issues = models.TextField(null=True, blank=True)

    def _str_(self):
        return f"{self.appointment.patient} - {self.appointment.provider} - {self.appointment.scheduled_datetime.strftime('%Y-%m-%d %H:%M')}"


# Analytics Models
class AnalyticsData(BaseModel):
    """Model for storing analytics data"""
    date = models.DateField()
    data_type = models.CharField(max_length=50, choices=(
        ('patient_stats', _('Patient Statistics')),
        ('consultation_stats', _('Consultation Statistics')),
        ('emergency_stats', _('Emergency Statistics')),
        ('maternal_stats', _('Maternal Health Statistics')),
    ))
    data = models.JSONField()  # Store analytics data as JSON

    def _str_(self):
        return f"{self.data_type} - {self.date}"