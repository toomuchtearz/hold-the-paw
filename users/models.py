from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    class RoleChoice(models.TextChoices):
        PERSONAL = "personal", "Personal account"
        SHELTER = "shelter", "Shelter"

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_validator,],
        max_length=17,
    )
    telegram_nickname = models.CharField(max_length=64, blank=True, null=True)

    role = models.CharField(
        choices=RoleChoice.choices,
        default=RoleChoice.PERSONAL,
        max_length=20,
    )


class ShelterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shelter_profile")

    company_name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField(blank=True)


class PersonalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="personal_profile")
