from rest_framework import viewsets, status

from apps.api.filters.application import ApplicationFilter
from apps.organizations.models import Application, Employee
from apps.api.serializers import ApplicationSerializer, ApplicationUpdateSerializer, ApplicationListSerializer, ApplicationListUpdateSerializer
from apps.api.paginatior import ContentPaginator
from django_filters.rest_framework import DjangoFilterBackend


class ApplicationViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.UpdateModelMixin,
):
    """ViewSet заявок сотрудника"""

    queryset = Application.objects.all().order_by("-created_at")
    serializer_classes = {
        "list": ApplicationSerializer,
        "update": ApplicationUpdateSerializer
    }
    pagination_class = ContentPaginator

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ApplicationSerializer)

    def get_queryset(self):
        user = self.request.user
        queryset = Application.objects.filter(employee__user=user).order_by(
            "-created_at"
        )
        return queryset


    def perform_create(self, serializer):
        user = self.request.user
        employee = Employee.objects.get(user=user)
        serializer.save(employee=employee)


class ApplicationListViewSet(viewsets.mixins.ListModelMixin,
                             viewsets.mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    queryset = Application.objects.all().order_by("-created_at")
    serializer_classes = {
        "list": ApplicationListSerializer,
        "update": ApplicationListUpdateSerializer,
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ApplicationSerializer)