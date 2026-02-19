from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from pets.models import PetListing
from pets.serializers import PetListingListSerializer, PetListingRetrieveSerializer


class PetListingViewSet(viewsets.ModelViewSet):
    queryset = PetListing.objects.all()
    serializer_class = PetListingListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = PetListingRetrieveSerializer

        return serializer
