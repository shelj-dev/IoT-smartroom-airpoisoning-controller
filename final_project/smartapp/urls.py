from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  
    path("graph/", views.graph, name="graph"),
    path("logs/", views.logs, name="logs"),
    path("about/", views.about, name="about"),
    path("help/", views.help_page, name="help"),

    path("api/get-sensor/", views.receive_sensor_data),
    path("update-threshold/", views.update_threshold, name="update_threshold"),
]