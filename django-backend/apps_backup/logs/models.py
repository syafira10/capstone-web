from django.db import models

class ActivityLog(models.Model):
    user = models.CharField(max_length=100)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class ErrorLog(models.Model):
    error = models.TextField()
    severity = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
