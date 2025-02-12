


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import *

def index(request):
    return render(request,'index.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')

        appointment = Appointment.objects.create(
            patient=request.user.patient,
            date=date,
            time=time,
            reason=reason,
            status='PENDING'
        )

        # Send email notification
        send_appointment_confirmation(appointment)

        return JsonResponse({'status': 'success'})

    return render(request, 'booking.html')


def subscribe_consultation(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        subscription, created = Subscription.objects.get_or_create(
            email=email
        )

        if created:
            # Send welcome email
            send_welcome_email(email)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

def patient_list(request):
    the_patients = Patient.objects.all()
    # context = {'patient_list':the_patients}
    return render(request,'patients.html',{'patient_list':the_patients})
