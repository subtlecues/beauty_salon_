from django.urls import path
from salon_admin import views

app_name = 'salon_admin'

urlpatterns = [
    path('', views.main, name='adm_main'),
    path('bookings/', views.bookings, name='adm_bookings'),
    path('services/', views.services, name='adm_services'),
    path('services/<str:service_name>', views.service, name='adm_service'),
    path('specialists/', views.specialists, name='adm_specialists'),
    path('specialist/<int:specialist_id>', views.specialist, name='adm_specialist'),
]