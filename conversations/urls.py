from django.urls import path, include
from rest_framework.routers import DefaultRouter

from conversations.views import ConversationViewSet

app_name = "conversations"


router = DefaultRouter()
router.register("", ConversationViewSet, basename="conversations")

urlpatterns = [
    path("", include(router.urls))
]
