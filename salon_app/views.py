from django.shortcuts import render
from django.views.generic import DetailView


def home(request):
    return render(request, 'salon_app/home.html')


def services(request):
    return render(request, 'salon_app/services.html')


def service(request, service_name):
    return render(request, 'salon_app/service.html', {'title': service_name})


def specialists(request):
    return render(request, 'salon_app/specialists.html')


def specialist(request, specialist_id):
    return render(request, 'salon_app/specialists.html', {'title': specialist_id})


def booking(request, user_id, service_name, booking_time):
    if request.method == 'POST':
        pass
    return render(request, 'salon_app/booking.html', {'title': 'booking'})