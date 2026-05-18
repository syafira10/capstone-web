from django.db import models

class HistoricalData(models.Model):
    station = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    rain = models.FloatField()
    water_level_krl = models.FloatField()
    water_level_kai = models.FloatField()
    status = models.CharField(max_length=20)
