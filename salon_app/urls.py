from django.contrib import admin
from django.urls import path
from salon_app import views

app_name = 'salon_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<str:service_name>/', views.service, name='service'),
    path('specialists/', views.specialists, name='specialists'),
    path('specialists/<int:specialist_id>/', views.specialist, name='specialist'),
    path('booking/', views.booking, name='booking'),
    path('panel/', views.booking, name='panel')
    ]
