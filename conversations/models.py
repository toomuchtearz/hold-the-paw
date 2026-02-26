from django.conf import settings
from django.db import models

from pets.models import PetListing


class Conversation(models.Model):
    pet_listing = models.ForeignKey(PetListing, on_delete=models.CASCADE, related_name="conversations")
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at",]
        unique_together = ["pet_listing", "adopter",]

    def __str__(self) -> str:
        return f"Chat: {self.adopter.email} about {self.pet_listing.name}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Message from {self.sender.email} at {self.created_at}"
