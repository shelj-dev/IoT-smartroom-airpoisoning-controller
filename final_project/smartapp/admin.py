from django.contrib import admin

from .models import SensorData
from .models import Limit


admin.site.register(SensorData)
admin.site.register(Limit)