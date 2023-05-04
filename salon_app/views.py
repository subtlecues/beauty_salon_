from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def root_handler(request):
    return render(request, "index.html")
    # return HttpResponse("Hello, world. You are at the index page.")

def services_handler(request):
    return HttpResponse("Hello, world. You are at the salon services page.")

def service_id_handler(request, service_id):
    return HttpResponse(f"Hello, world. You are at the page for salon service {service_id}.")

