from apps.api.serializers import OriginalImageSerializer
from rest_framework import viewsets, status



class FaceIdViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    """ViewSet отметки FaceID"""
    serializer_class = OriginalImageSerializer

