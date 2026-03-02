from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters

from pets.models import PetListing
from pets.serializers import PetListingListSerializer, PetListingRetrieveSerializer, PetListingCreateSerializer


class PetListingViewSet(viewsets.ModelViewSet):
    queryset = PetListing.objects.all()
    serializer_class =  PetListingCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    ordering_fields = ("created_at",)
    search_fields = ("name", "location")

    filterset_fields = (
        "id",
        "breed",
        "pet_type",
        "age",
        "gender",
        "special_needs",
        "has_passport",
        "is_vaccinated",
        "is_sterilized",
        "color",
        "status",

    )
    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = PetListingRetrieveSerializer
        elif self.action == "list":
            serializer = PetListingListSerializer

        return serializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
