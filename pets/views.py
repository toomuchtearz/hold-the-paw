from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters

from pets.models import PetListing
from pets.permissions import IsAuthorOrReadOnly
from pets.serializers import PetListingListSerializer, PetListingRetrieveSerializer, PetListingCreateSerializer


class PetListingViewSet(viewsets.ModelViewSet):
    queryset = PetListing.objects.all()
    serializer_class =  PetListingCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
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

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]

        return super().get_permissions()

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "retrieve":
            serializer = PetListingRetrieveSerializer
        elif self.action == "list":
            serializer = PetListingListSerializer

        return serializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.filter(
                is_active=True
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MyListingsListView(ListAPIView):
    queryset = PetListing.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PetListingListSerializer

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_fields = ("is_active", "status")
    ordering_fields = ("created_at",)
    search_fields = ("name", "location")

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)
