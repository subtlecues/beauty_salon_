import os

from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_salon.settings')
import django
from django.conf import settings

if not settings.configured:
    django.setup()
from django.test import TestCase, Client
from salon_admin.utilities import available_time_slots
from datetime import datetime, timezone
from salon_app.models import *
from salon_admin.views import reservation
from salon_admin.forms import BookingForm



class TestAvailableTimeSlots(TestCase):
    def test_available_time_slots_Equal_result(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = available_time_slots(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:15', '2023-04-06 09:30']
        self.assertEqual(result, expected_result)

        end_period = datetime.strptime('2023-04-06 13:00', '%Y-%m-%d %H:%M')
        serv_duration = 60
        booked_time = [
            [datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 11:00', '%Y-%m-%d %H:%M')]
        ]
        result = available_time_slots(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:00', '2023-04-06 11:00', '2023-04-06 11:15',
                           '2023-04-06 11:30', '2023-04-06 11:45', '2023-04-06 12:00']
        self.assertEqual(result, expected_result)

    def test_available_time_slots_List_of_string_result(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = available_time_slots(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:15', '2023-04-06 09:30']
        self.assertTrue(result, expected_result)

    def test_available_time_slots_Wrong_step_value(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = available_time_slots(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:10','2023-04-06 09:15', '2023-04-06 09:30', '2023-04-06 09:40']
        self.assertNotIn(result, expected_result)

    def test_available_time_slots_Raise_incorrect_input_period(self):
        end_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        start_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        with self.assertRaises(AttributeError):
            available_time_slots(serv_duration, start_period, end_period, booked_time)

    def test_available_time_slots_Empty_booked_list(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = []
        serv_duration = 30
        result = available_time_slots(serv_duration, start_period, end_period, booked_time)
        expected_result = ['2023-04-06 09:00', '2023-04-06 09:15', '2023-04-06 09:30']
        self.assertEqual(result, expected_result)

    def test_available_time_slots_Empty_free_time_result(self):
        start_period = datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M')
        end_period = datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')
        booked_time = [
            [datetime.strptime('2023-04-06 09:00', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M')],
            [datetime.strptime('2023-04-06 09:15', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 09:45', '%Y-%m-%d %H:%M')],
            [datetime.strptime('2023-04-06 09:45', '%Y-%m-%d %H:%M'),
             datetime.strptime('2023-04-06 10:00', '%Y-%m-%d %H:%M')]
        ]
        serv_duration = 30
        result = available_time_slots(serv_duration, start_period, end_period, booked_time)
        expected_result = []
        self.assertEqual(result, expected_result)


class TestEndpoint(TestCase):
    def test_booking_status_200(self):
        c = Client()
        service = Service.objects.create(name='Manicure',
                                         price=150.0,
                                         duration=30)
        service.save()
        specialist = Specialist.objects.create(name='Jenny',
                                               rank=1,
                                               phone='+108003736566',
                                               status=2)
        specialist.services.add(service)
        specialist.save()

        response = c.post(reverse('salon_admin:reservation'), {
            'specialist': specialist.id,
            'service': service.id,
            'customer': 1,
            'booking_from': '2023-04-10 10:00',
            'booking_to': '2023-04-10 11:00',
            'phone': '+123456789',
            'status': 2,
            'comment': 'Test comment'
        })

        self.assertEqual(response.status_code, 302)

        booking = Booking.objects.get(specialist=specialist, service=service)
        expected_booking_from = datetime(2023, 4, 10, 10, 0, tzinfo=timezone.utc)
        self.assertEqual(booking.booking_from, expected_booking_from)