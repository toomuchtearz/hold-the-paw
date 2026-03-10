from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from pets.models import PetListing, PetListingImage


class PetListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetListingImage
        fields  = (
            "id",
            "image",
        )


class PetListingCreateSerializer(serializers.ModelSerializer):
    additional_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True, required=False
    )

    class Meta:
        model = PetListing
        fields = (
            "id",
            "name",
            "location",
            "pet_type",
            "gender",
            "age",
            "color",
            "breed",
            "is_sterilized",
            "is_vaccinated",
            "special_needs",
            "has_passport",
            "story",
            "about",
            "status",
            "main_image",
            "additional_images",
        )

    @transaction.atomic
    def create(self, validated_data):
        additional_images = validated_data.pop("additional_images", [])
        pet_listing = PetListing.objects.create(**validated_data)

        for image in additional_images:
            PetListingImage.objects.create(
                image=image,
                pet_listing=pet_listing
            )


        return pet_listing


class PetListingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetListing
        fields = (
            "id",
            "name",
            "gender",
            "age",
            "main_image",
        )


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "phone_number",
            "telegram_nickname",
            "role",
        )


class PetListingRetrieveSerializer(serializers.ModelSerializer):
    additional_images = PetListingImageSerializer(
        many=True, read_only=True
    )
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = PetListing
        fields = (
            "id",
            "name",
            "location",
            "pet_type",
            "gender",
            "age",
            "breed",
            "color",
            "is_sterilized",
            "is_vaccinated",
            "special_needs",
            "has_passport",
            "story",
            "about",
            "main_image",
            "additional_images",
            "author",
        )
