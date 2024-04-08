from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.organizations.models import WorkShift, EmployeePosition


User = get_user_model()
class UserEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")
class EmployeeWorkShiftSerializers(serializers.ModelSerializer):
    employee = serializers.SerializerMethodField()
    class Meta:
        model = EmployeePosition
        fields = ('employee',)

    def get_employee(self, obj):
        return f"{obj.employee.user.first_name} {obj.employee.user.last_name}"

class WorkShiftSerializer(serializers.ModelSerializer):
    """Сериализатор смен сотрудников"""
    employees_count = serializers.SerializerMethodField(method_name='get_employees_count')
    class Meta:
        model = WorkShift
        fields = ('id', "name", "schedule", 'employees_count')

    def get_employees_count(self, instance):
        employees_count = EmployeePosition.objects.filter(work_shift=instance).count()
        return employees_count

class WorkShiftDetailSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField(method_name='get_employees')

    class Meta:
        model = WorkShift
        fields = ("name", "schedule", 'employees')

    def get_employees(self, instance):
        employees = EmployeePosition.objects.filter(work_shift=instance)
        return EmployeeWorkShiftSerializers(employees, many=True).data

