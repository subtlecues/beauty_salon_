from django.contrib import admin
from django.urls import path
import salon_app.views

urlpatterns = [
    path("", salon_app.views.root_handler),
    path("services/", salon_app.views.services_handler),
    path("services/<int:service_id>/", salon_app.views.service_id_handler),
]
