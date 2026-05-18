from django.db import models

class Notification(models.Model):
    message = models.TextField()
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
