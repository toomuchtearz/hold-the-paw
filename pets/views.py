from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response

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

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=serializers.Serializer
    )
    def is_helped_toggle(self, request, pk=None):
        listing = self.get_object()
        listing.is_helped = not listing.is_helped
        listing.save()
        return Response(
            {"is_helped": listing.is_helped},
            status=status.HTTP_200_OK
        )

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=serializers.Serializer
    )
    def is_active_toggle(self, request, pk=None):
        listing = self.get_object()
        listing.is_active = not listing.is_active
        listing.save()
        return Response(
            {"is_active": listing.is_active},
            status=status.HTTP_200_OK
        )


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
