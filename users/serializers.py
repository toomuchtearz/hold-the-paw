from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import ShelterProfile, PersonalProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
            "is_staff",
        )
        read_only_fields = (
            "id",
            "is_staff",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        updated_user = super().update(instance, validated_data)

        if password:
            updated_user.set_password(password)
            updated_user.save()

        return updated_user


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "phone_number",
            "password",
            "role",
        )

        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "style": {"input_type": "password"},
            }
        }
    def create(self, validated_data):

        new_user = get_user_model().objects.create_user(**validated_data)
        new_user_role = new_user.role

        if new_user_role == get_user_model().RoleChoice.SHELTER:
            ShelterProfile.objects.create(
                user=new_user
            )
        elif new_user_role == get_user_model().RoleChoice.PERSONAL:
            PersonalProfile.objects.create(user=new_user)

        return new_user


class UserManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )

class ShelterManageSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="shelter_profile.company_name")
    address = serializers.CharField(source="shelter_profile.address")
    description = serializers.CharField(source="shelter_profile.description")

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "company_name",
            "address",
            "description",
            "phone_number",
        )

    def update(self, instance, validated_data):
        shelter_profile_info = validated_data.pop("shelter_profile")
        shelter_profile = instance.shelter_profile
        updated_user = super().update(instance, validated_data)

        if shelter_profile_info:

            for key, value in shelter_profile_info.items():
                setattr(shelter_profile, key, value)

            shelter_profile.save()

        return updated_user


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid': 'Password must be at least 8 characters long with at least one capital letter and symbol'}
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
