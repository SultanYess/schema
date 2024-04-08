from rest_framework import viewsets
from apps.api.serializers import WorkShiftSerializer, WorkShiftDetailSerializer
from apps.api.paginatior import ContentPaginator
from apps.organizations.models import WorkShift


class WorkShiftViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet смен"""
    queryset = WorkShift.objects.all().order_by("-created_at")
    serializer_classes = {
        "list": WorkShiftSerializer,
        'retrieve': WorkShiftDetailSerializer,
    }
    pagination_class = ContentPaginator

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, WorkShiftSerializer)
