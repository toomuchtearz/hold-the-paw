from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from pets.models import PetListing
from pets.serializers import PetListingListSerializer, PetListingRetrieveSerializer, PetListingCreateSerializer


class PetListingViewSet(viewsets.ModelViewSet):
    queryset = PetListing.objects.all()
    serializer_class =  PetListingCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = PetListingRetrieveSerializer
        elif self.action == "list":
            serializer = PetListingListSerializer

        return serializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
