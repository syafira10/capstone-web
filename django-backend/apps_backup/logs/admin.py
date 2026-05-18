from django.contrib import admin
from .models import ActivityLog, ErrorLog

admin.site.register(ActivityLog)
admin.site.register(ErrorLog)
