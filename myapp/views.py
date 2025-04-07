from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone

from resource.models import EducationalResource
from .forms import UserRegistrationForm, PatientProfileForm, AppointmentForm, MedicalRecordForm, DoctorProfileForm, \
    DoctorSignUpForm
from .models import NutritionLog, Patient, Appointment, MedicalRecord

from django.db.models import Q

def home(request):
    resources = EducationalResource.objects.all().order_by('-created_at')[:3]
    return render(request, 'landing/main.html', {'resources': resources})

def services(request):
    return render(request, 'landing/service.html')

def pricing(request):
    return render(request,'landing/pricing.html')

def testimonial(request):
    return render(request,'landing/testimonial.html')

def contact(request):
    return render(request,'landing/contact.html')

def get_started(request):
    return render(request,'landing/get-started.html')





# Authentication views
def register_patient(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = PatientProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            patient = profile_form.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = PatientProfileForm()

    return render(request, 'auth/patient_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def register_provider(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = DoctorSignUpForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            provider = profile_form.save(commit=False)
            provider.user = user
            provider.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('provider_dashboard')
    else:
        user_form = UserRegistrationForm()
        profile_form = DoctorProfileForm()

    return render(request, 'auth/provider_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            if hasattr(user, 'patient_profile'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'provider_profile'):
                return redirect('provider_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'auth/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

@login_required
def update_appointment(request, appointment_id):
    # Your code to handle updating an appointment
    # For example:
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_detail', appointment_id=appointment_id)
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'update_appointment.html', {'form': form})

# Patient views
@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')

    upcoming_appointments = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=timezone.now(),
        status='scheduled'
    ).order_by('appointment_date')

    recent_records = MedicalRecord.objects.filter(
        patient=patient
    ).order_by('-date')[:5]

    return render(request, 'patient/patient_dashboard.html', {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'recent_records': recent_records
    })

# views.py - update book_appointment view
from datetime import datetime


@login_required
def book_appointment(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Get cleaned data including the combined appointment_date
            appointment = form.save(commit=False)

            # Debug print statements
            print(f"Form is valid: {form.cleaned_data}")
            print(f"Appointment date from form: {form.cleaned_data.get('appointment_date')}")

            # Make sure appointment_date is set
            if form.cleaned_data.get('appointment_date'):
                appointment.appointment_date = form.cleaned_data.get('appointment_date')

            appointment.patient = patient
            appointment.status = 'scheduled'
            appointment.save()
            messages.success(request, "Appointment scheduled successfully!")
            return redirect('patient_dashboard')
        else:
            # Print form errors for debugging
            print(f"Form errors: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = AppointmentForm()

    return render(request, 'book-appointment.html', {
        'form': form,
    })

@login_required
def view_appointments(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')

    status = request.GET.get('status', '')
    if status:
        appointments = Appointment.objects.filter(patient=patient, status=status).order_by('-appointment_date')
    else:
        appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')

    return render(request, 'patient/appointments.html', {
        'appointments': appointments,
        'current_status': status
    })

@login_required
def view_medical_records(request):
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')

    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-date')

    return render(request, 'patient/records.html', {
        'medical_records': medical_records
    })

# Provider views
@login_required
def provider_dashboard(request):
    try:
        provider = request.user.provider_profile
    except:
        messages.error(request, "You are not registered as a healthcare provider.")
        return redirect('home')

    today = timezone.now().date()
    today_appointments = Appointment.objects


@login_required
def patient_details(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    # Check if the user has permission to view this patient
    # Option 1: Only allow if it's the user's own profile
    if request.user == patient.user:
        # Context dictionary to pass to template
        context = {
            'patient': patient,
            # Calculate age based on date_of_birth if needed
            # Other derived data can be added here
        }
        return render(request, 'patient/patient_detail.html', context)
    else:
        # If not authorized, redirect or show access denied
        # You might want to modify this based on your requirements
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You don't have permission to view this patient's details.")


@login_required
def add_medical_record(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    # Get the healthcare provider associated with the current user
    try:
        provider = request.user.healthcare_profile
    except:
        messages.error(request, "You must be a registered healthcare provider to add medical records.")
        return redirect('patient_detail', patient_id=patient_id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            # Create medical record but don't save to DB yet
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.provider = provider
            medical_record.date = timezone.now()
            medical_record.save()

            messages.success(request, "Medical record added successfully.")
            return redirect('patient_detail', patient_id=patient_id)
    else:
        # Pre-fill the patient field
        form = MedicalRecordForm()

    context = {
        'form': form,
        'patient': patient
    }
    return render(request, 'patient/add_medical_record.html', context)


def add_resource(request):
    return None

@login_required
def patient_recommendations(request):
    """View for displaying personalized health recommendations to patients"""
    try:
        # Get the patient profile for the current user
        patient = Patient.objects.get(user=request.user)
        
        # Get recent nutrition logs (last 7 days)
        recent_logs = NutritionLog.objects.filter(
            patient=patient,
            date__gte=datetime.now().date() - timedelta(days=7)
        )
        
        # Initialize recommendation engine
        recommender = MaternalHealthRecommender()
        
        # Get personalized recommendations
        recommendations = recommender.get_personalized_recommendations(
            patient, recent_logs
        )
        
        context = {
            'patient': patient,
            'recommendations': recommendations,
        }
        
        return render(request, 'maternal_health/recommendations.html', context)
    
    except Patient.DoesNotExist:
        # If the user is not a patient, show appropriate message
        context = {
            'error': 'You need a patient profile to access recommendations.'
        }
        return render(request, 'maternal_health/error.html', context)