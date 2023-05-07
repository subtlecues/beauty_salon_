from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from salon_app.models import Service, Specialist, WorkSchedule, Booking
from .forms import ServiceForm, SpecialistForm, WorkScheduleForm, BookingForm

def main(request):
    return render(request, 'salon_admin/main.html', {'title': 'Administration page'})

def bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'salon_admin/bookings.html', {'title': 'Bookings page', 'bookings': bookings})

def services(request):
    services = Service.objects.all()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServiceForm()
    return render(request, 'salon_admin/services.html', {'title': 'Services page', 'services': services, 'form': form})

def service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'salon_admin/service.html', {'title': service.name, 'service': service})

def specialists(request):
    specialists = Specialist.objects.all()
    if request.method == 'POST':
        form = SpecialistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialists')
    else:
        form = SpecialistForm()
    return render(request, 'salon_admin/specialists.html', {'title': 'Specialists page', 'specialists': specialists, 'form': form})

def specialist(request, specialist_id):
    specialist = get_object_or_404(Specialist, pk=specialist_id)
    schedules = WorkSchedule.objects.filter(specialist=specialist)
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            work_schedule = form.save(commit=False)
            work_schedule.specialist = specialist
            work_schedule.save()
            return redirect('specialist', specialist_id=specialist_id)
    else:
        form = WorkScheduleForm()
    return render(request, 'salon_admin/specialist.html', {'title': specialist.name, 'specialist': specialist, 'schedules': schedules, 'form': form})

def reservation(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookings')
    else:
        form = BookingForm()
    return render(request, 'salon_admin/reservation.html', {'title': 'Reservation', 'form': form})

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServiceForm()
    return render(request, 'salon_admin/add_service.html', {'form': form})

def add_specialist(request):
    if request.method == 'POST':
        form = SpecialistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialists')
    else:
        form = SpecialistForm()
    return render(request, 'salon_admin/specialist.html', {'form': form})

def add_work_schedule(request):
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialists')
    else:
        form = WorkScheduleForm()
    return render(request, 'salon_admin/add_work_schedule.html', {'form': form})
