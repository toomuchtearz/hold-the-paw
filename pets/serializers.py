from rest_framework import serializers

from pets.models import PetListing


class PetListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetListing
        fields = "__all__"
