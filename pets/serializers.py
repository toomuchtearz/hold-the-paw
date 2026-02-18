from django.db import transaction
from rest_framework import serializers

from pets.models import Ad, Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"

