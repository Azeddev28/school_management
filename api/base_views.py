from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend


class BaseModelViewset(ModelViewSet):
    filterset_fields = '__all__'
    ordering_fields = '__all__'
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = '__all__'
