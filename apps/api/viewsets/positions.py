from rest_framework import viewsets
from apps.organizations.models import PositionName
from apps.api.serializers import PositionSerializer
from apps.api.paginatior import ContentPaginator


class PositionViewSet(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet позиций"""
    queryset = PositionName.objects.all()
    serializer_class = PositionSerializer
    pagination_class = ContentPaginator

