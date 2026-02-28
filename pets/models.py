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


def create_custom_path_pet_listing_image(instance, filename):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads/images/",
        f"{slugify(instance.pet_listing.name)}-{uuid.uuid4()}{extension}"
    )


class PetListing(models.Model):
    class AgeChoices(models.TextChoices):
        PUPPY = "puppy", "Puppy (0–12 months)"
        JUNIOR = "junior", "Junior (1 - 2 years)"
        ADULT = "adult", "Adult (3–5 years)"
        SENIOR = "senior", "Senior (5+ years)"

    class TypeChoices(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = 'cat', "Cat"
        HAMSTER = 'hamster', "Hamster"
        BIRD = "bird", "Bird"
        FISH = "fish", "Fish"
        OTHER = 'other', 'Other'

    class ColorChoices(models.TextChoices):
        WHITE = 'white', "White"
        BEIGE = "beige", "Beige"
        GRAY = 'gray', "Gray"
        BLACK = "black", "Black"
        GINGER = 'ginger', 'Ginger'
        BROWN = 'brown', 'Brown'
        BRINDLE = "brindle", "Brindle"
        SPOTTED = "spotted", "Spotted"
        TWO_COLOR = "two_color", "Two colored"
        TRICOLOR = "tricolor", "Tricolor"
        MULTICOLORED = "multicolor", "Multicolored"
        OTHER = "other", "Other"

    class GenderChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        UNKNOWN = "unknown", "Unknown"

    class StatusChoices(models.TextChoices):
        HOME = "looking_for_a_home", "Looking for a home"
        HELP = "help_needed", "Help needed"

    class BreedChoices(models.TextChoices):
        NO_BREED = "no_breed", "No breed"
        MONGREL = "mongrel", "Mongrel"
        PUREBRED = "purebred", "Purebred"

    class SizeChoices(models.TextChoices):
        SMALL = "s", "Small"
        MEDIUM = "m", "Medium"
        LARGE = "l", "Large"

    # --- Pet Details ---
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=64)

    gender = models.CharField(
        max_length=32,
        choices=GenderChoices.choices,
        default=GenderChoices.UNKNOWN
    )

    age = models.CharField(
        max_length=32,
        choices=AgeChoices.choices,
    )

    breed = models.CharField(
        max_length=32,
        choices=BreedChoices.choices
    )

    pet_type = models.CharField(
        max_length=32,
        default=TypeChoices.DOG,
        choices=TypeChoices.choices
    )

    main_image = models.ImageField(upload_to=create_custom_path)

    color = models.CharField(
        max_length=32,
        choices=ColorChoices.choices
    )

    is_sterilized = models.BooleanField(default=False)
    is_vaccinated = models.BooleanField(default=False)
    special_needs = models.BooleanField(default=False)
    has_passport = models.BooleanField(default=False)

    story = models.TextField(null=True, blank=True, max_length=1024)
    about = models.TextField(null=True, blank=True, max_length=1024)

    # --- Listing Details ---
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )

    status = models.CharField(
        max_length=32,
        choices=StatusChoices.choices,
        default=StatusChoices.HOME
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Listing for {self.name}"


class PetListingImage(models.Model):
    pet_listing = models.ForeignKey(
        PetListing, on_delete=models.CASCADE,
        related_name="additional_images"
    )
    image = models.ImageField(
        upload_to=create_custom_path_pet_listing_image,
    )
