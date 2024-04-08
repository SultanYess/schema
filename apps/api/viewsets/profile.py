from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets, status
from apps.organizations.models import Employee, Application, EmployeeEvent, Event
from apps.api.serializers import (
    ProfileSerializer,
    EmplpoyeeApplicationSerializer,
    ChangeEventSerializer,
    GetLastEventSerializer,
)
from rest_framework.response import Response
from rest_framework import permissions
from apps.fr.models import RecognizedFace

class ProfileViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet Профиля"""

    queryset = Employee.objects.filter()
    serializer_classes = {
        "list": ProfileSerializer,
        "create":EmplpoyeeApplicationSerializer
    }

    def post(self, request, format=None):
        serializer = EmplpoyeeApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ProfileSerializer)

    def get_queryset(self):
        queryset = Employee.objects.filter(user=self.request.user)
        return queryset


class ChangeLastEventViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
):
    """Viewset последних активностей"""

    serializer_classes = {
        "list": GetLastEventSerializer,
        "create": ChangeEventSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ChangeEventSerializer)

    def get_queryset(self):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        return EmployeeEvent.objects.filter(employee=employee).order_by("-created_at")[:1]

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            employee = Employee.objects.get(user=request.user)
            serializer.save(employee=employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=Application)
def create_employee_event(sender, instance, created, **kwargs):
    if instance.application_status == "approved":
        employee_event = EmployeeEvent.objects.create(
            employee=instance.employee,
            event_type=instance.type,
            event_note=instance.comment,
            event_start_date=instance.date,
        )
        Event.objects.create(
            employee=instance.employee,
            employee_event=employee_event,
        )
