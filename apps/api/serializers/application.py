from rest_framework import serializers
from apps.organizations.models import Application, Employee


class ApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор отправки заявки для изменений времени активности сотрудника"""
    class Meta:
        model = Application
        fields = ("id", "date", "type", "comment", "application_status")

    def create(self, validated_data):
        user = self.context["request"].user
        employee = Employee.objects.get(user=user)
        validated_data["employee"] = employee
        return Application.objects.create(**validated_data)
class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "date", "type", "comment", "application_status")

class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "date", "type", "comment", "application_status")

class ApplicationListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "date", "type", "comment", "application_status")

