from django.contrib import admin

# Register your models here.
from .models import SensorData
from .models import Limit


admin.site.register(SensorData)
admin.site.register(Limit)