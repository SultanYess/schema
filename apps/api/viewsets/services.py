from rest_framework import viewsets, generics

from apps.organizations import StructureUnitTypes
from apps.organizations.models import StructureUnit
from apps.api.serializers import ServiceSerializer, ServiceDetailSerializers
from apps.api.paginatior import ContentPaginator


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet департаментов """
    queryset = StructureUnit.objects.filter(type=StructureUnitTypes.DEPARTMENT)
    serializer_classes = {
        "list": ServiceSerializer,
        "retrieve": ServiceDetailSerializers
    }
    pagination_class = ContentPaginator
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ServiceSerializer)
