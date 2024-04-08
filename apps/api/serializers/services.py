from rest_framework import serializers

from apps.organizations.models import StructureUnit, EmployeePosition, Employee
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
class EmployeeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class ServiceListSerializer(serializers.ModelSerializer):
    leader_first_name = serializers.CharField(source='employee.user.first_name')
    leader_last_name = serializers.CharField(source='employee.user.last_name')
    class Meta:
        model = EmployeePosition
        fields = (
            'leader_first_name',
            'leader_last_name'
        )
class ServiceEmployeeSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source='employee.user.first_name')
    employee_last_name = serializers.CharField(source='employee.user.last_name')
    position_name = serializers.CharField(source='structure_unit.position_name')
    leader_parent_name = serializers.CharField(source='structure_unit.parent')
    leader_parent_parent_name = serializers.CharField(source='structure_unit.parent.parent')

    class Meta:
        model = EmployeePosition
        fields = (
            'leader_parent_name',
            'leader_parent_parent_name',
            'employee_first_name',
            'employee_last_name',
            'position_name',
            'active_from',
        )

class ServiceEmployeeDetailSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source='employee.user.first_name')
    employee_last_name = serializers.CharField(source='employee.user.last_name')
    position = serializers.CharField(source='structure_unit.position_name')

    class Meta:
        model = EmployeePosition
        fields = ('employee_first_name', 'employee_last_name', "position")


class ServiceSerializer(serializers.ModelSerializer):
    """Сериализатор департамента"""
    department_name = serializers.SerializerMethodField()
    department_leader = serializers.SerializerMethodField(method_name='get_leader_name')
    employee_count = serializers.SerializerMethodField(method_name='get_employee_count')


    class Meta:
        model = StructureUnit
        fields = ("id", "type", "department_name", "is_department_leader", 'department_leader', 'employee_count')

    def get_employee_count(self, instance):
        department_name = instance.department_name
        structure_unit = StructureUnit.objects.filter(department_name=department_name)
        employee_count = EmployeePosition.objects.filter(structure_unit__in=structure_unit).count()
        return employee_count


    def get_department_name(self, obj):
        return obj.department_name.name if obj.department_name else None


    def get_leader_name(self, instance):
        department_name = instance.department_name
        structure_units = StructureUnit.objects.filter(
            department_name=department_name,
            is_department_leader=True
        )
        employees = EmployeePosition.objects.filter(structure_unit__in=structure_units)
        serializer = ServiceListSerializer(employees, many=True)
        return serializer.data

class ServiceDetailSerializers(serializers.ModelSerializer):
    """Детальный сериализатор департамента"""

    employees = serializers.SerializerMethodField(method_name="get_employees")
    department_leader = serializers.SerializerMethodField(method_name="get_department_leader")
    class Meta:
        model = StructureUnit
        fields = ("department_leader", "employees")

    def get_employees(self, instance):
        employee_positions = EmployeePosition.objects.filter(
            structure_unit__department_name=instance.department_name,
        )
        serializer = ServiceEmployeeDetailSerializer(employee_positions, many=True)
        return serializer.data

    def get_department_leader(self, instance):
        department_name = instance.department_name
        parent_organization = instance.organization
        structure_unit = StructureUnit.objects.filter(
            department_name=department_name,
            is_department_leader=True,
            organization=parent_organization,
        )
        employees = EmployeePosition.objects.filter(structure_unit__in=structure_unit)
        serializer = ServiceEmployeeSerializer(employees, many=True)
        return serializer.data
