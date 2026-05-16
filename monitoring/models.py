from django.db import models

class FloodData(models.Model):

    STATUS_CHOICES = [
        ('AMAN', 'AMAN'),
        ('KRL STOP', 'KRL STOP'),
        ('TOTAL STOP', 'TOTAL STOP'),
    ]

    rain_value = models.FloatField()

    krl_water_level = models.FloatField()

    kai_water_level = models.FloatField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.status} - {self.created_at}"