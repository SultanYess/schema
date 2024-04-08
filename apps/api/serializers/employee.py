from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.organizations.models import WorkShift

from apps.organizations.models import (
    Employee,
    EmployeePosition,
    EmployeeEvent,
    Organization,
    StructureUnit,
)

User = get_user_model()


# UTILS
class EmployeeDepartmentSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    class Meta:
        model = EmployeePosition
        fields = [
            "department_name",
        ]
    def get_department_name(self, obj):
        structure_unit = obj.structure_unit
        if structure_unit and structure_unit.department_name:
            return structure_unit.department_name.name
        return None
class EmployeeWorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = [
            'work_shift'
        ]
class EmployeeUpdateWorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = "__all__"

class EmployeePositionSerializer(serializers.ModelSerializer):
    position_names = serializers.CharField(source="get_position_name", read_only=True)
    department_name = serializers.CharField(source="get_department_name", read_only=True)
    parent = serializers.CharField(source="get_organization_name", read_only=True)

    # department_name = serializers.SerializerMethodField()
    class Meta:
        model = EmployeePosition
        fields = [
            "structure_unit",
            "position_names",
            "department_name",
            "active_from",
            "active_to",
            "parent",
        ]

    def get_position_name(self, obj):
        if obj.structure_unit:
            return obj.structure_unit.position_name.name
        return None

    def get_department_name(self, obj):
        if obj.structure_unit:
            return obj.structure_unit.department_name
        return None

    def get_organization_name(self, obj):
        if obj.structure_unit:
            return obj.structure_unit.organization
        return None

class EmployeeListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="structure_unit.department_name")

    class Meta:
        model = EmployeePosition
        fields = ["structure_unit"]


class EmployeeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeEvent
        fields = ["event_type", "event_start_date"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "name",
        ]


class StructureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructureUnit
        fields = ("position_name", "department_name")


class UserEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "phone", "iin", "groups")








# MAIN
class EmployeeUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновлений Employee"""
    user = UserSerializer()
    work_shift = serializers.SerializerMethodField(method_name="get_work_shift")
    class Meta:
        model = Employee
        fields = (
            "id",
            "user",
            "work_shift",
        )

    def get_work_shift(self, obj):
        work_shift = obj.work_shift.all()
        serializer = EmployeeUpdateWorkShiftSerializer(work_shift, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserSerializer(
                instance.user, data=user_data, partial=True
            )
            if user_serializer.is_valid():
                user_serializer.save()
                return super().update(instance, validated_data)
            else:
                raise serializers.ValidationError(user_serializer.errors)
        else:
            return super().update(instance, validated_data)

class EmployeeSerializer(serializers.ModelSerializer):
    """Список сотрудников Employee"""
    user = UserEmployeeSerializer()
    positions = EmployeeDepartmentSerializer(many=True)
    work_shift_name = serializers.SerializerMethodField(method_name="get_work_shift_name")
    class Meta:
        model = Employee
        fields = (
            "id",
            "user",
            "positions",
            "work_shift_name",
        )
    def get_work_shift_name(self, instance):
        positions = instance.positions.all()
        work_shift_names = []
        for position in positions:
            work_shift = position.work_shift
            if work_shift:
                work_shift_names.append(work_shift.name)
        return work_shift_names


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор сотрудников"""

    events = EmployeeEventSerializer(many=True)
    user = UserSerializer()
    organization = OrganizationSerializer()
    position_name = serializers.SerializerMethodField()
    positions = EmployeePositionSerializer(many=True)

    class Meta:
        model = Employee
        fields = (
            "id",
            "user",
            "position_name",
            "organization",
            "employment_type",
            "positions",
            "active_from",
            "active_to",
            "events",
        )

    def get_events(self, obj):
        events = obj.events.order_by("-created_at")
        serializers = EmployeeEventSerializer(instance=events, many=True)
        return serializers.data

    def get_position_name(self, obj):
        latest_position = obj.positions.order_by("-created_at").first()
        if latest_position:
            structure_unit = latest_position.structure_unit
            if structure_unit:
                return structure_unit.position_name.name
        return None

