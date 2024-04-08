from rest_framework import serializers
from apps.api.serializers import *
from apps.organizations.models import Application
from apps.api.serializers import UserSerializer
from apps.organizations.models import Event

class ProfilePositionSerializer(serializers.ModelSerializer):
    position_name = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = EmployeePosition
        fields = ('position_name', 'department_name', 'active_from', 'active_to')

    def get_position_name(self, obj):
        structure_unit = obj.structure_unit
        if structure_unit and structure_unit.position_name:
            return structure_unit.position_name.name
        return None
    def get_department_name(self,obj):
        structure_unit = obj.structure_unit
        if structure_unit and structure_unit.department_name:
            return structure_unit.department_name.name
        return None

class EventSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.user.username')
    employee_event = serializers.CharField(source='employee_event.event_type')
    # recognized_face = serializers.CharField(source='recognized_face.face_image')
    class Meta:
        model = Event
        fields = ('id', 'employee', 'recognized_face', 'employee_event')

class ProfileSerializer(serializers.ModelSerializer):
    """Сериализтор профиля"""
    profile_event = serializers.SerializerMethodField(method_name='get_profile_event')
    user = UserSerializer()
    organization = OrganizationSerializer(read_only=True)
    positions = ProfilePositionSerializer(many=True)
    position_name = serializers.SerializerMethodField()
    last_events = EmployeeEventSerializer(many=True, read_only=True)
    work_shift_name = serializers.SerializerMethodField(method_name='get_work_shift_name')


    def get_profile_event(self, instance):
        events = Event.objects.filter(employee=instance)
        serializer = EventSerializer(events, many=True)
        return serializer.data
    def get_position(self, obj):
        positions = obj.positions.order_by("-created_at")[:5]
        serializers = EmployeePositionSerializer(instance=positions, many=True)
        return serializers.data

    def get_last_position(self, obj):
        last_positions = obj.positions.order_by("-created_at")[:1]
        serializers = EmployeePositionUtilsSerializer(
            instance=last_positions, many=True
        )
        return serializers.data


    def get_last_events(self, obj):
        last_events = obj.events.filter(event_type__in=["coming", "leaving"]).order_by("-created_at")[:2]
        serializers = EmployeeEventUtilsSerializer(instance=last_events, many=True)
        return serializers.data

    def get_position_name(self, obj):
        latest_position = obj.positions.order_by("-created_at").first()
        if latest_position:
            structure_unit = latest_position.structure_unit
            if structure_unit:
                return structure_unit.position_name.name
        return None

    def get_work_shift_name(self, instance):
        positions = instance.positions.all()
        work_shift_data = []
        for position in positions:
            work_shift = position.work_shift
            if work_shift:
                work_shift_data.append({
                    'work_shift_name': work_shift.name,
                    'work_shift_schedule': work_shift.schedule
                })
        return work_shift_data



    class Meta:
        model = Employee
        fields = (
            "id",
            "organization",
            "user",
            "position_name",
            "last_events",
            "active_from",
            "employment_type",
            "positions",
            "profile_event",
            "work_shift_name",
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # rep['last_positions'] = self.get_last_position(instance)
        rep["last_events"] = self.get_last_events(instance)
        return rep

class EmplpoyeeApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'employee', 'date', 'type', 'comment')

    def create(self, validated_data):
        user = self.context['request'].user
        employee = user.employees.first()
        if employee:
            validated_data['employee'] = employee
            return Application.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("User has no associated employee.")

class GetLastEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeEvent
        fields = ("employee", "event_type", "event_start_date", "event_note")


class ChangeEventSerializer(serializers.ModelSerializer):
    """Сериализатор изменений последнего приход ухода"""

    class Meta:
        model = Application
        fields = ("id", "employee", "type", "date", "comment", "application_status")
