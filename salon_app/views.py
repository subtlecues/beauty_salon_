from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from salon_app.models import Service, Specialist, WorkSchedule, Booking
from datetime import datetime, timedelta
from salon_admin.utilities import available_time_slots

TIMEDELTA = timedelta(days=7)
CURRENT_TIME = datetime.today()
REQUIRED_PERIOD = CURRENT_TIME + TIMEDELTA


def home(request):
    return render(request, 'salon_app/home.html')


def services(request):
    all_services = {}

    try:
        all_services = Service.objects.all()

    except Exception as err:
        print(err)

    return render(request, 'salon_app/services.html', {'services': all_services})

def one_service(request, service_name, specialist_id=None):
    service_details = {}
    available_specialists = {}

    try:
        service_details = Service.objects.filter(name=service_name).first()
        service_id = service_details.id
        service_duration = service_details.duration

        if not specialist_id:
            available_specialists = \
                Specialist.objects.filter(status=2,
                                          services__id=service_id,
                                          workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                          ).distinct().values('id', 'name').order_by('name')
        else:
            available_specialists = Specialist.objects.filter(id=specialist_id,
                                                              status=2,
                                                              workschedule__end_time__gt=CURRENT_TIME
                                                              ).distinct().values('id', 'name')
        print(available_specialists)
        for specialist in available_specialists:
            specialist_id = specialist['id']
            available_booking = []
            work_day = WorkSchedule.objects.filter(specialist_id=specialist_id,
                                                   end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                                   ).values('begin_time', 'end_time').order_by('begin_time')

            for period in work_day:
                booked_time_list = []
                booked_time = Booking.objects.filter(specialist_id=specialist_id,
                                                     booking_to__range=(period['begin_time'], period['end_time'])
                                                     ).values('booking_from', 'booking_to').order_by('booking_from')

                for busy in booked_time:
                    booked_time_list.append([busy['booking_from'], busy['booking_to']])

                free_time = available_time_slots(service_duration=service_duration,
                                                      start_time=period['begin_time'],
                                                      end_time=period['end_time'],
                                                      booked_time=booked_time_list)

                available_booking.extend(free_time)
            specialist.update({'available_booking': available_booking})
            print(service_details)
            print(available_specialists)
            print(available_specialists.query)

    except Exception as err:
        print(f'One_service error:\n{err}')

    return render(request, 'salon_app/service.html', {'service_details': service_details,
                                                  'specialists': available_specialists})

def service(request, service_name):
    service_id = None
    service_details = {}
    available_specialists = {}

    try:
        service_details = Service.objects.filter(name=service_name).all()
        for detail in service_details:
            service_id = detail.id
        available_specialists = \
            Specialist.objects.filter(status=2,
                                      services__id=service_id,
                                      workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                      ).distinct().order_by('name')
        print(available_specialists.query)
    except Exception as err:
        print(err)

    return render(request, 'salon_app/service.html', {'service_details': service_details,
                                                  'specialists': available_specialists})


def specialists(request):
    available_specialists = {}

    try:
        available_specialists = Specialist.objects.filter(status=2,
                                                          # workschedule__end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                                          ).distinct()
    except Exception as err:
        print(err)

    return render(request, 'salon_app/specialists.html', {'specialists': available_specialists})





def specialist_detail(request, name):
    service_duration = {}  # dictionary to store duration of each service provided by the specialist
    available_services = {}  # dictionary to store all the services provided by the specialist and their durations
    available_booking = {}  # dictionary to store available time slots for each service

    try:
        # Get the specialist object using the name passed to the view
        specialist = Specialist.objects.filter(name=name).first()
        specialist_id = specialist.id

        # Get all the services provided by the specialist and their durations
        services = Service.objects.filter(specialist__id=specialist_id).values('id', 'name', 'duration')
        for service in services:
            available_services[service['name']] = service['duration']
            service_duration[service['id']] = service['duration']

        # For each service, get the available time slots for the specialist
        for service_id, duration in service_duration.items():
            available_time = []
            work_day = WorkSchedule.objects.filter(specialist_id=specialist_id,
                                                   end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)
                                                   ).values('begin_time', 'end_time').order_by('begin_time')

            for period in work_day:
                booked_time_list = []
                booked_time = Booking.objects.filter(specialist_id=specialist_id,
                                                     service_id=service_id,
                                                     booking_to__range=(period['begin_time'], period['end_time'])
                                                     ).values('booking_from', 'booking_to').order_by('booking_from')

                for busy in booked_time:
                    booked_time_list.append([busy['booking_from'], busy['booking_to']])

                free_time = available_time_slots(service_duration=duration,
                                                 start_time=period['begin_time'],
                                                 end_time=period['end_time'],
                                                 booked_time=booked_time_list)

                available_time.extend(free_time)

            available_booking[Service.objects.get(id=service_id).name] = available_time

            print(Service.objects.filter(specialist__id=specialist_id).query)
            print(WorkSchedule.objects.filter(specialist_id=specialist_id,
                                              end_time__range=(CURRENT_TIME, REQUIRED_PERIOD)).query)
            print(Booking.objects.filter(specialist_id=specialist_id, service_id=service_id,
                                         booking_to__range=(period['begin_time'], period['end_time'])).query)



    except Exception as err:
        print(f'One_specialist error:\n{err}')

    return render(request, 'salon_app/specialist.html', {'specialist': specialist,
                                                         'available_services': available_services,
                                                         'available_booking': available_booking}
                  )


def specialist(request, specialist_id):
    try:
        specialist_detail = Specialist.objects.get(status=2, id=specialist_id)
        services = specialist_detail.services.all()
        context = {'specialist': specialist_detail, 'services': services}

        # Get the available time slots for the first service of the specialist
        if services:
            service = services.first()
            booked_time = []  # Replace with the booked time slots for the specialist
            start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            end_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
            available_time = available_time_slots(service.duration, start_time, end_time, booked_time)
            context['available_time'] = available_time

        return render(request, 'salon_app/specialist.html', context)

    except Specialist.DoesNotExist:
        return render(request, 'salon_app/specialist_not_found.html')



def booking(request, service_name, specialist_id):
    if request.method == 'POST':
        try:
            service = Service.objects.filter(name=service_name).get()
            service_duration = service.duration
            comment = request.POST['comment']
            booking_from = request.POST['booking_time']
            booking_to = datetime.strptime(booking_from, '%Y-%m-%d %H:%M') + timedelta(minutes=service_duration)

            current_booking = Booking(customer=1,
                                      phone='+380991234556',
                                      status=2,
                                      service_id=service.id,
                                      specialist_id=specialist_id,
                                      booking_from=booking_from,
                                      booking_to=booking_to,
                                      comment=comment)
            current_booking.save()
            return render(request, 'salon_app/booking_successful.html')
        except Exception as err:
            print(f'Booking saving error:\n{err}')
            return redirect(one_service, service_name, specialist_id)


