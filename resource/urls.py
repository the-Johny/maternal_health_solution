from django.urls import path
from . import views

urlpatterns = [
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('resources/add/', views.add_resource, name='add_resource'),
    path('resources/<int:resource_id>/edit/', views.edit_resource, name='edit_resource'),
]
