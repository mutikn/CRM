from django.contrib import admin
from attendance.models import QrCode, Attendance

admin.site.register(QrCode)
admin.site.register(Attendance)