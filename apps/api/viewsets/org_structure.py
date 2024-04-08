from rest_framework import viewsets
from apps.organizations.models import StructureUnit
from apps.api.serializers import OrgStructureSerializer


class OrgStructureViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """ViewSet структуры организаций"""
    queryset = StructureUnit.objects.all()
    serializer_class = OrgStructureSerializer
