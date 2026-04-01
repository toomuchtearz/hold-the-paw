from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import ShelterProfile, PersonalProfile

class PersonalRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "phone_number",
            "password",
            'full_name',
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "validators": [validate_password],
            },
            "full_name": {"required": True, "allow_blank": False},
        }

    @transaction.atomic
    def create(self, validated_data):
        validated_data["role"] = get_user_model().RoleChoice.PERSONAL
        full_name = validated_data.pop("full_name")
        new_user = get_user_model().objects.create_user(**validated_data)


        PersonalProfile.objects.create(
            user=new_user,
            full_name=full_name
        )
        return new_user


class ShelterRegistrationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(write_only=True)
    tax_id = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "phone_number",
            "password",
            "tax_id",
            "company_name",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "validators": [validate_password],
            }
        }
    @transaction.atomic
    def create(self, validated_data):
        company_name = validated_data.pop("company_name")
        tax_id = validated_data.pop("tax_id")
        validated_data["role"] = get_user_model().RoleChoice.SHELTER

        new_user = get_user_model().objects.create_user(**validated_data)
        ShelterProfile.objects.create(
            user=new_user,
            company_name=company_name,
            tax_id=tax_id
        )
        return new_user


class PersonalManageSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="personal_profile.full_name")

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "full_name",
            "phone_number",
            "telegram_nickname",
            "viber_phone_number",
            "role",
        )
        read_only_fields = ("role", "email")

    def update(self, instance, validated_data):
        personal_profile_info = validated_data.pop("personal_profile", {})
        personal_profile = instance.personal_profile
        updated_user = super().update(instance, validated_data)

        if personal_profile_info:

            for key, value in personal_profile_info.items():
                setattr(personal_profile, key, value)

            personal_profile.save()

        return updated_user


class ShelterManageSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="shelter_profile.company_name")
    address = serializers.CharField(source="shelter_profile.address")
    description = serializers.CharField(source="shelter_profile.description")
    tax_id = serializers.CharField(source="shelter_profile.tax_id")

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "company_name",
            "address",
            "description",
            "phone_number",
            "viber_phone_number",
            "telegram_nickname",
            "tax_id",
            "role",
        )
        read_only_fields = ("role", "email",)

    def update(self, instance, validated_data):
        shelter_profile_info = validated_data.pop("shelter_profile", {})
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
    new_password = serializers.CharField(
        max_length=128, write_only=True,
        style={"input_type": "password"},
        validators=[validate_password]

    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=128, write_only=True,
        style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        max_length=128, write_only=True,
        style={"input_type": "password"},
        validators=[validate_password]
    )
