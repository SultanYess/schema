from rest_framework import serializers

from django.db.models import Count
from apps.organizations.models import PositionName
from apps.organizations.models import EmployeePosition
class PositionEmployeeSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source='employee.user.first_name')
    employee_last_name = serializers.CharField(source='employee.user.last_name')
    class Meta:
        model = EmployeePosition
        fields = ('employee_first_name', 'employee_last_name')


class PositionSerializer(serializers.ModelSerializer):
    """Сериализатор должностей"""
    employee_position_count = serializers.SerializerMethodField(method_name='get_employee_position_count')
    class Meta:
        model = PositionName
        fields = (
            "id",
            "name",
            "employee_position_count"
        )

    def get_employee_position_count(self, instance):
        structure_units = instance.structure_units.all()
        positions = EmployeePosition.objects.filter(structure_unit__in=structure_units)
        employee_position_counts = positions.aggregate(total_employee_count=Count('employee'))
        return employee_position_counts['total_employee_count']
