from django.db import transaction
from rest_framework import serializers

from pets.models import Ad, Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"

class AdSerializer(serializers.ModelSerializer):
    pet = PetSerializer()

    class Meta:
        model = Ad
        fields = (
            "id",
            "created_at",
            "pet"
        )

    def create(self, validated_data):
        with transaction.atomic():
            pet_info = validated_data.pop("pet")
            new_pet = Pet.objects.create(**pet_info)
            new_ad = Ad.objects.create(
                **validated_data,
                pet=new_pet
            )
            return new_ad
