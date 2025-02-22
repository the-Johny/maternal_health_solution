from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from .models import (
    Patient,
    Appointment,
    EmergencyAlert, VirtualConsultation, PregnancyConsultation
)


def index(request):
    return render(request, 'index.html')


@login_required
def book_appointment(request):
    if request.method == 'POST':
        try:
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            appointment_type = request.POST.get('appointment_type')
            notes = request.POST.get('notes', '')
            is_virtual = request.POST.get('is_virtual', False)

            # Combine date and time into datetime
            date_time_str = f"{date_str} {time_str}"
            appointment_date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

            # Get the patient's healthcare provider
            # You might want to implement logic to assign or select a provider
            provider = request.user.patient.preferredprovider if hasattr(request.user.patient,
                                                                         'preferredprovider') else None

            if not provider:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No healthcare provider assigned'
                }, status=400)

            # Create the appointment
            appointment = Appointment.objects.create(
                patient=request.user.patient,
                provider=provider,
                appointment_type=appointment_type,
                appointment_date=appointment_date,
                notes=notes,
                is_virtual=is_virtual,
                status='SCHEDULED'
            )

            # If it's a virtual consultation, create the related record
            if is_virtual:
                VirtualConsultation.objects.create(
                    patient=request.user.patient,
                    provider=provider,
                    appointment_date=appointment_date,
                    meeting_link=f"https://meet.example.com/{appointment.id}",
                    status='SCHEDULED'
                )

            # You can add email notification logic here
            # send_appointment_confirmation(appointment)

            return JsonResponse({
                'status': 'success',
                'appointment_id': appointment.id
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    # GET request - render booking form
    return render(request, 'book-appointment.html')


@login_required
def patient_list(request):
    patients = Patient.objects.all().select_related('user')

    # Format patient data for template
    patient_data = []
    for patient in patients:
        appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
        latest_appointment = appointments.first()

        patient_data.append({
            'id': patient.id,
            'name': patient.user.get_full_name(),
            'phone': patient.phone_number,
            'blood_type': patient.blood_type,
            'latest_appointment': latest_appointment.appointment_date if latest_appointment else None,
            'total_appointments': appointments.count()
        })

    return render(request, 'patients.html', {
        'patient_list': patient_data
    })


@login_required
def create_pregnancy_consultation(request):
    if request.method == 'POST':
        try:
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            pregnancy_week = int(request.POST.get('pregnancy_week'))
            notes = request.POST.get('notes', '')

            # Validate pregnancy week
            if not 1 <= pregnancy_week <= 45:
                raise ValueError("Invalid pregnancy week")

            # Combine date and time
            date_time_str = f"{date_str} {time_str}"
            appointment_date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

            # Get the provider (you might want to implement provider selection logic)
            provider = request.user.patient.preferredprovider if hasattr(request.user.patient,
                                                                         'preferredprovider') else None

            if not provider:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No healthcare provider assigned'
                }, status=400)

            # Create the consultation
            consultation = PregnancyConsultation.objects.create(
                patient=request.user.patient,
                provider=provider,
                appointment_date=appointment_date,
                pregnancy_week=pregnancy_week,
                notes=notes,
                status='SCHEDULED'
            )

            return JsonResponse({
                'status': 'success',
                'consultation_id': consultation.id
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return render(request, 'pregnancy_consultation.html')


@login_required
def create_emergency_alert(request):
    if request.method == 'POST':
        try:
            alert_type = request.POST.get('alert_type')
            description = request.POST.get('description')
            location = request.POST.get('location', '')

            alert = EmergencyAlert.objects.create(
                patient=request.user.patient,
                alert_type=alert_type,
                description=description,
                location=location,
                status='ACTIVE'
            )

            # Here you might want to add notification logic for healthcare providers
            # notify_providers_of_emergency(alert)

            return JsonResponse({
                'status': 'success',
                'alert_id': alert.id
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return render(request, 'emergency-alert.html')


@login_required
def dashboard(request):
    # Get patient's data for dashboard
    patient = request.user.patient

    context = {
        'upcoming_appointments': Appointment.objects.filter(
            patient=patient,
            appointment_date__gte=timezone.now(),
            status='SCHEDULED'
        ).order_by('appointment_date')[:5],

        'pregnancy_consultations': PregnancyConsultation.objects.filter(
            patient=patient
        ).order_by('-appointment_date')[:5],

        'virtual_consultations': VirtualConsultation.objects.filter(
            patient=patient
        ).order_by('-appointment_date')[:5],

        'emergency_alerts': EmergencyAlert.objects.filter(
            patient=patient
        ).order_by('-created_at')[:5]
    }

    return render(request, 'dashboard.html', context)
