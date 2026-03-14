from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard,name="dashboard"),
    path("api/get-sensor/", views.receive_sensor_data),
]