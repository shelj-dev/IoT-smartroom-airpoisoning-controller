from django.db import models

class SensorData(models.Model):
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
class Limit(models.Model):
    threshold = models.IntegerField()