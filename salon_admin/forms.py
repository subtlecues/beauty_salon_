from django import forms
from django.forms.widgets import DateTimeInput
from salon_app.models import Service, Specialist, WorkSchedule, Booking


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'price', 'duration')


class SpecialistForm(forms.ModelForm):
    class Meta:
        model = Specialist
        fields = ('name', 'rank', 'phone', 'status', 'services')
        widgets = {
            'services': forms.CheckboxSelectMultiple(),
        }


# class WorkScheduleForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['specialist'].queryset = Specialist.objects.all()
#
#     class Meta:
#         model = WorkSchedule
#         fields = ['specialist', 'date', 'begin_time', 'end_time']

# class WorkScheduleForm(forms.ModelForm):
#     class Meta:
#         model = WorkSchedule
#         fields = ['specialist', 'begin_time', 'end_time', 'date']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['specialist'].queryset = Specialist.objects.all()
#
#     def clean(self):
#         cleaned_data = super().clean()
#         specialist = cleaned_data.get("specialist")
#         date = cleaned_data.get("date")
#         begin_time = cleaned_data.get("begin_time")
#         end_time = cleaned_data.get("end_time")
#
#         existing_schedule = WorkSchedule.objects.filter(specialist=specialist, date=date).exists()
#         if existing_schedule:
#             raise forms.ValidationError(f"There is already a work schedule for {specialist.name} on {date}")
#
#         if begin_time >= end_time:
#             raise forms.ValidationError("Begin time must be before end time")
#
#         return cleaned_data
#
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.date = self.cleaned_data['date']
#         if commit:
#             instance.save()
#         return instance
class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = ['specialist', 'begin_time', 'end_time']
        widgets = {
            'begin_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }




class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['specialist', 'service', 'customer', 'booking_from', 'booking_to', 'phone', 'status', 'comment']
        widgets = {
            'booking_from': DateTimeInput(attrs={'type': 'datetime-local'}),
            'booking_to': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
