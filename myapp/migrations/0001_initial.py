# Generated by Django 4.2 on 2025-02-17 15:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('data_type', models.CharField(choices=[('patient_stats', 'Patient Statistics'), ('consultation_stats', 'Consultation Statistics'), ('emergency_stats', 'Emergency Statistics'), ('maternal_stats', 'Maternal Health Statistics')], max_length=50)),
                ('data', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('scheduled_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('reason', models.TextField()),
                ('is_virtual', models.BooleanField(default=False)),
                ('meeting_link', models.URLField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppointmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration_minutes', models.PositiveIntegerField(default=30)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HealthcareProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('specialization', models.CharField(max_length=100)),
                ('qualification', models.CharField(max_length=255)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('phone_number', models.CharField(max_length=15)),
                ('availability', models.JSONField(default=dict)),
                ('is_available_for_virtual', models.BooleanField(default=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='providers', to='myapp.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='provider_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('diagnosis', models.TextField()),
                ('prescription', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='medical_records', to='myapp.appointment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Newborn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('birth_weight', models.DecimalField(decimal_places=2, max_digits=4)),
                ('birth_length', models.DecimalField(decimal_places=1, max_digits=4)),
                ('apgar_score', models.CharField(blank=True, max_length=10, null=True)),
                ('complications', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('blood_type', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=5, null=True)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('chronic_conditions', models.TextField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VirtualConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('meeting_platform', models.CharField(choices=[('zoom', 'Zoom'), ('teams', 'Microsoft Teams'), ('google_meet', 'Google Meet'), ('other', 'Other')], max_length=50)),
                ('meeting_id', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_password', models.CharField(blank=True, max_length=50, null=True)),
                ('recording_url', models.URLField(blank=True, null=True)),
                ('technical_issues', models.TextField(blank=True, null=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='virtual_consultation', to='myapp.appointment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PregnancyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateField()),
                ('start_date', models.DateField()),
                ('is_high_risk', models.BooleanField(default=False)),
                ('risk_factors', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pregnancy_records', to='myapp.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PregnancyConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('week_of_pregnancy', models.PositiveIntegerField()),
                ('blood_pressure', models.CharField(blank=True, max_length=20, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('fetal_heart_rate', models.PositiveIntegerField(blank=True, null=True)),
                ('observations', models.TextField(blank=True, null=True)),
                ('recommendations', models.TextField(blank=True, null=True)),
                ('appointment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.appointment')),
                ('pregnancy_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='myapp.pregnancyrecord')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pregnancy_consultations', to='myapp.healthcareprovider')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostpartumSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('delivery_date', models.DateField()),
                ('physical_recovery', models.TextField(blank=True, null=True)),
                ('mental_health', models.TextField(blank=True, null=True)),
                ('lactation_support', models.TextField(blank=True, null=True)),
                ('nutritional_guidance', models.TextField(blank=True, null=True)),
                ('recommendations', models.TextField(blank=True, null=True)),
                ('appointment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.appointment')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postpartum_support', to='myapp.patient')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postpartum_support', to='myapp.healthcareprovider')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewbornScreening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('screening_date', models.DateField()),
                ('screening_type', models.CharField(max_length=100)),
                ('results', models.TextField()),
                ('is_normal', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('follow_up_needed', models.BooleanField(default=False)),
                ('follow_up_notes', models.TextField(blank=True, null=True)),
                ('newborn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenings', to='myapp.newborn')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newborn_screenings', to='myapp.healthcareprovider')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newborn',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newborns', to='myapp.patient'),
        ),
        migrations.CreateModel(
            name='MedicalRecordAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='medical_records/')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('medical_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='myapp.medicalrecord')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='medicalrecord',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='myapp.patient'),
        ),
        migrations.AddField(
            model_name='medicalrecord',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to='myapp.healthcareprovider'),
        ),
        migrations.CreateModel(
            name='GeneticCounselling',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('family_history', models.TextField()),
                ('genetic_tests', models.TextField(blank=True, null=True)),
                ('test_results', models.TextField(blank=True, null=True)),
                ('recommendations', models.TextField(blank=True, null=True)),
                ('follow_up_needed', models.BooleanField(default=False)),
                ('appointment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.appointment')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genetic_counselling', to='myapp.patient')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genetic_counselling', to='myapp.healthcareprovider')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmergencyAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('alert_type', models.CharField(choices=[('medical', 'Medical Emergency'), ('maternal', 'Maternal Emergency'), ('other', 'Other Emergency')], max_length=50)),
                ('description', models.TextField()),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('resolution_notes', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_alerts', to='myapp.patient')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.appointmenttype'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='myapp.patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='myapp.healthcareprovider'),
        ),
    ]
