from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('pricing/', views.pricing, name='pricing'),
    path('testimonials/', views.testimonial, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('get_started',views.get_started,name='get_started'),


    # Authentication
    path('register/patient/', views.register_patient, name='patient_register'),
    path('register/provider/', views.register_provider, name='provider_register'),
    path('login/', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    # Patient routes
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/appointments/book/', views.book_appointment, name='book_appointment'),
    path('patient/appointments/', views.view_appointments, name='view_appointments'),
    path('patient/medical-records/', views.view_medical_records, name='view_medical_records'),

    # Provider routes
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/appointments/', views.view_appointments, name='provider_appointments'),
    path('provider/appointments/<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
    # path('provider/patient/', views.manage_patients, name='manage_patients'),
    path('provider/patient/<int:patient_id>/', views.patient_details, name='patient_details'),
    path('provider/patient/<int:patient_id>/add-record/', views.add_medical_record, name='add_medical_record'),

]
