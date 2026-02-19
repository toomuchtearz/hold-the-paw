import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def create_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads/images/",
        f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    )


class PetListing(models.Model):
    class AgeChoices(models.TextChoices):
        PUPPY = "puppy", "Puppy (0–6/12 months)"
        JUNIOR = "junior", "Junior (6 months – 2 years)"
        ADULT = "adult", "Adult/Mature (1–7 years)"
        SENIOR = "senior", "Senior (6–10+ years)"

    class TypeChoices(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = 'cat', "Cat"
        HAMSTER = 'hamster', "Hamster"
        RABBIT = 'rabbit', 'Rabbit'
        OTHER = 'other', 'Other'

    class ColorChoices(models.TextChoices):
        BLACK = "black", "Black"
        WHITE = 'white', "White"
        GRAY = 'gray', "Gray"
        GINGER = 'ginger', 'Ginger'
        BROWN = 'brown', 'Brown'
        BEIGE = "beige", "Beige"
        TRICOLOR = "tricolor", "Tricolor"
        SPOTTED = "spotted", "Spotted"
        OTHER = "other", "Other"

    class GenderChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        UNKNOWN = "unknown", "Unknown"

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Looking for a home"
        PENDING = "pending", "Adoption pending"
        ADOPTED = "adopted", "Found a home"

    # --- Pet Details ---
    name = models.CharField(max_length=64)
    description = models.TextField()
    main_image = models.ImageField(upload_to=create_custom_path)
    location = models.CharField(max_length=256)

    age = models.CharField(
        max_length=64,
        choices=AgeChoices.choices,
    )

    pet_type = models.CharField(
        max_length=64,
        default=TypeChoices.DOG,
        choices=TypeChoices.choices
    )
    pet_type_details = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Please specify pet type if the main type field is 'Other'."
    )

    color = models.CharField(
        max_length=64,
        choices=ColorChoices.choices
    )
    color_details = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="Please specify color if the main color field is 'Other'"
    )

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.UNKNOWN
    )

    breed = models.CharField(max_length=64, null=True, blank=True)
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kg"
    )
    is_purebred = models.BooleanField(default=False)
    is_sterilized = models.BooleanField(default=False)
    is_vaccinated = models.BooleanField(default=False)

    # --- Listing Details ---
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Listing for {self.name}"
