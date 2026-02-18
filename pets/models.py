from django.db import models

class Pet(models.Model):
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

    name = models.CharField(max_length=64)
    description = models.TextField()
    main_image = models.ImageField(upload_to="media/")
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

    def __str__(self) -> str:
        return self.name
