from rest_framework import serializers
from apps.organizations.models import StructureUnit
from apps.organizations.models import EmployeePosition


class StructureEmployeeSerializer(serializers.ModelSerializer):
    employee_first_name = serializers.CharField(source='employee.user.first_name')
    employee_last_name = serializers.CharField(source='employee.user.last_name')
    position_name = serializers.CharField(source='structure_unit.position_name')
    leader_parent_name = serializers.CharField(source='structure_unit.parent')

    class Meta:
        model = EmployeePosition
        fields = (
            'leader_parent_name',
            'employee_first_name',
            'employee_last_name',
            'position_name',
            'active_from',
        )

class OrgStructureSerializer(serializers.ModelSerializer):
    """Сериализатор Структуры"""
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    parent_name = serializers.CharField(source='parent')

    class Meta:
        model = StructureUnit
        fields = (
            "parent_name",
            "priority",
            "type",
            "organization_name",
            "department",
            "position",
            "is_department_leader",
        )
    def get_position(self, obj):
        return obj.position_name.name if obj.position_name else None

    def get_department(self, obj):
        return obj.department_name.name if obj.department_name else None

    def get_organization_name(self, obj):
        return obj.organization.name if obj.organization else None
