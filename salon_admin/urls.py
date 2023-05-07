from django.urls import path
from . import views

app_name = 'salon_admin'
urlpatterns = [
    path('', views.main, name='main'),
    path('bookings/', views.bookings, name='bookings'),
    path('services/', views.services, name='services'),
    path('services/<str:service_name>/', views.service, name='service'),
    path('specialists/', views.specialists, name='specialists'),
    path('specialists/<int:specialist_id>/', views.specialist, name='specialist'),
    path('add_service/', views.add_service, name='add_service'),
    path('add_specialist/', views.add_specialist, name='add_specialist'),
    path('add_work_schedule/', views.add_work_schedule, name='add_work_schedule'),
    path('reservation/', views.reservation, name='reservation'),
]
