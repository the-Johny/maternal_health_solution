from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('api/book-appointment/', views.book_appointment, name='book_appointment'),
    path('api/subscribe/', views.subscribe_consultation, name='subscribe'),
    path('api/patient/all', views.patient_list, name='all-patients'),

]