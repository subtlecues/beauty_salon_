from datetime import datetime, timedelta
from salon_app.models import Booking, Specialist, Service

def get_available_time_slots(specialist_id=None, service_id=None):
    available_slots = {}
    today = datetime.now().date()
    for i in range(7):
        date = today + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        appointments = Booking.objects.filter(date=date)
        if specialist_id:
            specialist = Specialist.objects.get(id=specialist_id)
            specialist_name = specialist.name
            appointments = appointments.filter(specialist=specialist)
        else:
            specialist_name = None
        if service_id:
            service = Service.objects.get(id=service_id)
            service_name = service.name
            appointments = appointments.filter(service=service)
        else:
            service_name = None
        time_slots = []
        current_hour = datetime.now().hour
        for hour in range(current_hour, 20):
            for minute in range(0, 60, 15):
                time_str = f"{hour:02d}:{minute:02d}"
                if not appointments.filter(time=time_str).exists():
                    time_slots.append(time_str)
        if time_slots:
            available_slots[date_str] = {'specialist': specialist_name, 'service': service_name, 'time_slots': time_slots}
    return available_slots
