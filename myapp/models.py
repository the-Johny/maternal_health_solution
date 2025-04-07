from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    emergency_contact_name = models.CharField(max_length=100, default="Emergency Name")
    emergency_contact_phone = models.CharField(max_length=15, default="0700000000")
    due_date = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ], null=True, blank=True)
    # Additional fields for AI recommendations
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    pre_pregnancy_weight = models.FloatField(null=True, blank=True, help_text="Weight in kg before pregnancy")
    current_weight = models.FloatField(null=True, blank=True, help_text="Current weight in kg")
    is_first_pregnancy = models.BooleanField(default=True)
    has_diabetes = models.BooleanField(default=False)
    has_hypertension = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @property
    def pregnancy_week(self):
        if not self.due_date:
            return None
        today = date.today()
        # Assuming 40 weeks for full-term pregnancy
        days_until_due = (self.due_date - today).days
        if days_until_due > 280:  # Not pregnant yet
            return 0
        if days_until_due < 0:  # Past due date
            return 40
        weeks_remaining = days_until_due // 7
        return 40 - weeks_remaining


class Doctor(models.Model):
    # Doctor model remains unchanged
    SPECIALIZATION_CHOICES = [
        ('ob_gyn', 'Obstetrics/Gynecology'),
        ('pediatrics', 'Pediatrics'),
        ('general', 'General Practitioner'),
        ('cardiology', 'Cardiology'),
        ('endocrinology', 'Endocrinology'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    phone_number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50)
    years_of_experience = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class Admin(models.Model):
    # Admin model remains unchanged
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    phone_number = models.CharField(max_length=15)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Admin {self.user.first_name} {self.user.last_name}"


# models.py - update the Appointment model
class Appointment(models.Model):
    # Existing fields
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='appointments')
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('missed', 'Missed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)

    # New fields to match your template
    APPOINTMENT_TYPE_CHOICES = [
        ('GENERAL', 'General Consultation'),
        ('FOLLOWUP', 'Follow-up Visit'),
        ('SPECIALIST', 'Specialist Consultation'),
    ]
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='GENERAL')
    is_virtual = models.BooleanField(default=False)

    # Existing fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date']

    def __str__(self):
        return f"Appointment on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"


class MedicalRecord(models.Model):
    # MedicalRecord model remains unchanged but could be used for recommendations
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True, related_name='medical_records')
    date = models.DateTimeField(default=timezone.now)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    blood_pressure = models.CharField(max_length=20, null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Medical record for {self.patient} on {self.date.strftime('%Y-%m-%d')}"


# Add the new NutritionLog model
class NutritionLog(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='nutrition_logs')
    date = models.DateField(auto_now_add=True)
    calories = models.IntegerField()
    protein = models.FloatField(help_text="Protein in grams")
    carbs = models.FloatField(help_text="Carbohydrates in grams")
    fats = models.FloatField(help_text="Fats in grams")
    iron = models.FloatField(help_text="Iron in mg")
    calcium = models.FloatField(help_text="Calcium in mg")
    folate = models.FloatField(help_text="Folate in mcg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Nutrition log for {self.patient} on {self.date}"