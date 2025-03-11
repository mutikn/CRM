from django.contrib import admin
from attendance.models import QrCode, Attendance
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from report.models import Report  # Импортируйте вашу модель Report

# Инлайн для QR-кода
class QrCodeInline(admin.TabularInline):
    model = QrCode
    fields = ('qr_code',)
    readonly_fields = ('qr_code',)
    can_delete = False
    extra = 0

# Инлайн для посещаемости
class AttendanceInline(admin.TabularInline):
    model = Attendance
    fields = ('check_in', 'check_out')
    readonly_fields = ('check_in', 'check_out')
    can_delete = False
    extra = 0

# Инлайн для отчета
class ReportInline(admin.TabularInline):
    model = Report
    fields = ('date', 'message')
    readonly_fields = ('date', 'message')
    can_delete = False
    extra = 0
    def save_model(self, request, obj, form, change):
        # Присваиваем текущего пользователя как сотрудника (employee)
        obj.employee = request.user
        super().save_model(request, obj, form, change)

# Подключаем инлайны к пользовательской модели в админке
class CustomUserAdmin(UserAdmin):
    inlines = [QrCodeInline, AttendanceInline, ReportInline]  # Добавляем ReportInline
    list_display = UserAdmin.list_display + ('qr_code_display',)  # Добавляем отображение QR-кода

    def qr_code_display(self, obj):
        return obj.qrcode.qr_code if hasattr(obj, 'qrcode') else 'No QR Code'
    qr_code_display.short_description = 'QR Code'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            queryset = queryset.filter(id=request.user.id)  # Обычные staff видят только себя
        return queryset

# Регистрируем кастомного пользователя с инлайнами
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Оставляем регистрацию для остальных моделей
class QrCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'qr_code')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(user=request.user)  # Обычный staff видит только свои записи
        return queryset.none()

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'check_in', 'check_out')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        elif request.user.is_staff:
            return queryset.filter(user=request.user)  # Обычный staff видит только свои записи
        return queryset.none()

    def has_add_permission(self, request, obj=None):
        return False  # Обычные пользователи не могут добавлять записи

    # def has_delete_permission(self, request, obj=None):
    #     return False  # Обычные пользователи не могут удалять записи
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'message')

    exclude = ('employee',)  # Убираем поле из формы, но оно остается в базе

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Суперпользователь видит все отчеты
        return queryset.filter(employee=request.user)  # Сотрудники видят только свои отчеты

    def has_add_permission(self, request, obj=None):
        return request.user.is_staff  # Только сотрудники могут добавлять отчеты

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return obj is not None and obj.employee == request.user  # Разрешаем редактировать только свои отчеты

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Если отчет новый, присваиваем пользователя
            obj.employee = request.user
        super().save_model(request, obj, form, change)



admin.site.register(QrCode, QrCodeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Report, ReportAdmin)
