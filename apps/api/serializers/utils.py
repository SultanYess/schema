from rest_framework import serializers
from apps.organizations.models import EmployeePosition, EmployeeEvent, Organization


class EmployeePositionUtilsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = [
            "structure_unit",
            "active_from",
            "active_to",
        ]


class EmployeeEventUtilsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeEvent
        fields = ["event_type", "event_start_date"]


class OrganizationUtilsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "name",
        ]
