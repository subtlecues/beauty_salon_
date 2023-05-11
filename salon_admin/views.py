from django.shortcuts import render, redirect, get_object_or_404, reverse
from datetime import datetime, timedelta, date
from django.utils import timezone
from salon_app.models import Service, Specialist, WorkSchedule, Booking
from .forms import ServiceForm, SpecialistForm, WorkScheduleForm, BookingForm
from .utilities import get_available_time_slots, available_time_slots


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
            return redirect(reverse('salon_admin:services'))
    else:
        form = ServiceForm()
    return render(request, 'salon_admin/services.html', {'title': 'Services page', 'services': services, 'form': form})

def service(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'salon_admin/service.html', {'title': service.name, 'service': service})

def specialists(request):
    services = Service.objects.all()
    specialists = Specialist.objects.all()
    if request.method == 'POST':
        form = SpecialistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_admin:specialists')
    else:
        form = SpecialistForm()
    return render(request, 'salon_admin/specialists.html', {'title': 'Specialists page', 'specialists': specialists, 'form': form, 'services': services})

def specialist(request, specialist_id):
    specialist = get_object_or_404(Specialist, pk=specialist_id)
    schedules = WorkSchedule.objects.filter(specialist=specialist)
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            work_schedule = form.save(commit=False)
            work_schedule.specialist = specialist
            work_schedule.save()
            return redirect('salon_admin:specialist', specialist_id=specialist_id)
    else:
        form = WorkScheduleForm()
    return render(request, 'salon_admin/specialist.html', {'title': specialist.name, 'specialist': specialist, 'schedules': schedules, 'form': form})

def reservation(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_admin:bookings')
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
    services = Service.objects.all()
    if request.method == 'POST':
        form = SpecialistForm(request.POST)
        if form.is_valid():
            specialist = form.save(commit=False)
            specialist.save()
            selected_services = request.POST.getlist('services')
            for service_id in selected_services:
                service = Service.objects.get(pk=service_id)
                specialist.services.add(service)
            return redirect('salon_admin:specialists')
    else:
        form = SpecialistForm()
    return render(request, 'salon_admin/add_specialist.html', {'form': form, 'services': services})



def add_work_schedule(request):
    if request.method == 'POST':
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            specialist = form.cleaned_data['specialist']
            begin_time = form.cleaned_data['begin_time']
            end_time = form.cleaned_data['end_time']
            WorkSchedule.objects.create(
                specialist=specialist,
                begin_time=begin_time,
                end_time=end_time
            )
            return redirect('salon_admin:specialists')
    else:
        form = WorkScheduleForm(initial={'date': datetime.today()})
    return render(request, 'salon_admin/add_work_schedule.html', {'form': form})

from django.contrib import messages

def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    available_slots = get_available_time_slots(service_id=service_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.specialist = form.cleaned_data['specialist']
            booking.date = form.cleaned_data['date']
            booking.time = form.cleaned_data['time']
            booking.save()
            messages.success(request, 'Booking successful!')
            return redirect('salon_admin:service_detail', service_id=service_id)
    else:
        form = BookingForm()
    return render(request, 'salon_admin/service_detail.html', {'service': service, 'form': form, 'available_slots': available_slots})

def specialist_detail(request, specialist_id):
    specialist = get_object_or_404(Specialist, pk=specialist_id)
    available_slots = get_available_time_slots(specialist_id=specialist_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.specialist = specialist
            booking.service = form.cleaned_data['service']
            booking.date = form.cleaned_data['date']
            booking.time = form.cleaned_data['time']
            booking.save()
            messages.success(request, 'Booking successful!')
            return redirect('specialist_detail', specialist_id=specialist_id)
    else:
        form = BookingForm()
    return render(request, 'salon_admin/specialist_detail.html', {'specialist': specialist, 'form': form, 'available_slots': available_slots})
