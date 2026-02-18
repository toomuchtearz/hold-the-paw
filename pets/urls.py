from django.urls import path, include
from rest_framework.routers import DefaultRouter

from pets.views import AdViewSet

app_name = "pets"

router = DefaultRouter()

router.register("ads", AdViewSet, basename="ads")

urlpatterns = [
    path("", include(router.urls))
]
