from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.api.paginatior import ContentPaginator
from apps.organizations.models import Employee
from apps.api.serializers import (
    EmployeeDetailSerializer,
    EmployeeUpdateSerializer,
    EmployeeSerializer,
)


class EmployeeViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet сотрудников"""

    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_classes = {
        "list": EmployeeSerializer,
        "retrieve": EmployeeDetailSerializer,
        "partial_update": EmployeeUpdateSerializer,
    }
    pagination_class = ContentPaginator

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, EmployeeSerializer)
