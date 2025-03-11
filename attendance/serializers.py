from rest_framework import serializers
from .models import QrCode, Attendance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = ['id', 'user', 'qr_code']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'