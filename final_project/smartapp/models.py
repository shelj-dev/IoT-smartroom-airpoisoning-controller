from django.db import models

class GasReading(models.Model):

    gas_type = models.CharField(max_length=20, default="COMBUSTIBLE_GAS")
    value = models.FloatField()
    is_safe = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gas_type} {self.value}"