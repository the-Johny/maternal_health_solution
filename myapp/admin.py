from django.contrib import admin
from .models import Patient,Appointment,Subscription,ContactMessage
# Register your models here.
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Subscription)
admin.site.register(ContactMessage)