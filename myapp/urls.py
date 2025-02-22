from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('patients/', views.patient_list, name='patient_list'),
    path(
        'consultations/pregnancy/create/',
        views.create_pregnancy_consultation,
        name='create_pregnancy_consultation'
    ),
    path(
        'emergency/alert/create/',
        views.create_emergency_alert,
        name='create_emergency_alert'
    ),
    # path('api/book-appointment/', views.book_appointment, name='book_appointment'),
    # path('api/patient/all', views.patient_list, name='all-patients'),

]
