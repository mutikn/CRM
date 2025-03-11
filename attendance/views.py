import logging
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from attendance.models import QrCode, Attendance
from attendance.serializers import EmployeeSerializer, AttendanceSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = QrCode.objects.all()
    serializer_class = EmployeeSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'])

    @action(detail=False, methods=['post'])
    def scan_qr(self, request):
        username = request.data.get("username")
        if not username:
            return Response({"error": "Not logged in. Please log in!"}, status=400)

        try:
            qr_code = QrCode.objects.get(user__username=username)
            user = qr_code.user
            today = now().date()
            now_time = now()
            today_records = Attendance.objects.filter(user=user, check_in__date=today)

            if today_records.exists():
                record = today_records.first()
                if not record.check_out:
                    record.check_out = now_time
                    record.save()
                    return Response({"message": "Checked-out", "check_out": record.check_out})
                else:
                    return Response({"message": "Today has already been logged in and out"})
            else:
                Attendance.objects.create(user=user, check_in=now_time)
                return Response({"message": "Checked-in", "check_in": now_time})

        except QrCode.DoesNotExist:
            return Response({"error": "Employee not found!"}, status=404)
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return Response({"error": "Fatality!"}, status=500)

def qr_scanner(request):
    return render(request, "index.html")
