from django.urls import path
from . import views

app_name = 'salon_admin'
urlpatterns = [
    path('', views.main, name='main'),
    path('bookings/', views.bookings, name='bookings'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('specialists/', views.specialists, name='specialists'),
    path('specialists/<int:specialist_id>/', views.specialist_detail, name='specialist_detail'),
    # path('specialists/<specialist_name>/', views.specialist_detail, name='specialist_detail'),
    path('add_service/', views.add_service, name='add_service'),
    path('add_specialist/', views.add_specialist, name='add_specialist'),
    path('add_work_schedule/', views.add_work_schedule, name='add_work_schedule'),
    path('reservation/', views.reservation, name='reservation'),
]
