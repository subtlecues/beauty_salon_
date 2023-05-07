from django import forms
from salon_app.models import Service, Specialist, WorkSchedule, Booking


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'price', 'duration')


class SpecialistForm(forms.ModelForm):
    class Meta:
        model = Specialist
        fields = ('name', 'rank', 'phone', 'status', 'services')


class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = ['specialist', 'begin_time', 'end_time']



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('specialist', 'service', 'customer', 'date', 'time', 'phone')
