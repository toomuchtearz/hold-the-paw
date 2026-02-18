from rest_framework import viewsets

from pets.models import Ad
from pets.serializers import PetSerializer, AdSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
