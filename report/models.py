from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Report(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    message = models.TextField()

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.message}"
