from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.serializers import UserCreateSerializer, UserManageSerializer, ShelterManageSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserManageSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.role == get_user_model().RoleChoice.SHELTER:
            return ShelterManageSerializer
        return UserManageSerializer

    def get_object(self):
        return self.request.user


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)
