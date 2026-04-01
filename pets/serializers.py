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
            "is_helped",
            "is_active",
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
            "location",
            "is_active",
            "status",
        )


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "phone_number",
            "telegram_nickname",
            "viber_phone_number",
            "role",
        )


class PetListingRetrieveSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
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
            "author",
            "is_active",
            "status",
            "size",
            "photos",
        )

    def get_photos(self, obj):
        request = self.context.get('request')

        # Start with an empty list
        photo_list = []

        # Step A: Add the main image if it exists
        if obj.main_image:
            photo_list.append(request.build_absolute_uri(obj.main_image.url))

        # Step B: Loop through the gallery and add the rest
        # NOTE: Replace 'images' below with whatever your related_name is on the ForeignKey!
        # If you didn't set a related_name in models.py, it will be obj.petlistingimage_set.all()
        for gallery_img in obj.additional_images.all():
            if gallery_img.image:
                photo_list.append(request.build_absolute_uri(gallery_img.image.url))

        # Step C: Hand the final stitched list back to DRF
        return photo_list