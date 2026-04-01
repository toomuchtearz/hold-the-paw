from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pets.views import PetListingViewSet, MyListingsListView

app_name = "pets"

router = DefaultRouter()

router.register("listings", PetListingViewSet, basename="listings")

urlpatterns = [
    path("", include(router.urls)),
    path("my_listings/", MyListingsListView.as_view(), name="my-listings")
]
