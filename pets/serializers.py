from rest_framework import serializers

from pets.models import PetListing


class PetListingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetListing
        fields = (
            "id",
            "name",
            "status",
            "main_image",
            "location",
            "age",
            "pet_type",
            "color",
            "gender",
        )


class PetListingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetListing
        fields = "__all__"
