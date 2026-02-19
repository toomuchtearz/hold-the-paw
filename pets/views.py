from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from pets.models import PetListing
from pets.serializers import PetListingSerializer


class PetListingViewSet(viewsets.ModelViewSet):
    queryset = PetListing.objects.all()
    serializer_class = PetListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
