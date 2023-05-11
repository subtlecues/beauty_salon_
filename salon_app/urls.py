from django.contrib import admin
from django.urls import path
from salon_app import views
from salon_admin import views as admin_views

app_name = 'salon_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<str:service_name>/', views.one_service, name='one_service'),
    path('services/<str:service_name>/<int:specialist_id>/', views.one_service, name='one_service'),
    path('specialists/', views.specialists, name='specialists'),
    path('specialists/<int:specialist_id>/', views.specialist, name='specialist'),
    path('specialists/<str:name>/', views.specialist_detail, name='specialist_detail'),
    # path('specialists/<int:specialist_id>/', views.specialist, name='specialist'),
    path('booking/', views.booking, name='booking')
    ]
