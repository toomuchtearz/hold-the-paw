from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pets.views import PetListingViewSet, MyListingsViewSet

app_name = "pets"

router = DefaultRouter()

router.register("listings", PetListingViewSet, basename="listings")

urlpatterns = [
    path("", include(router.urls)),
    path("my_listings/", MyListingsViewSet.as_view(), name="my-listings")
]
