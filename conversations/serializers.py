from django.db import transaction
from rest_framework import serializers

from conversations.models import Conversation, Message


class MessageListSerializer(serializers.ModelSerializer):
    sender_email = serializers.CharField(source="sender.email", read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "sender_email",
            "text",
            "created_at",
        )


class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "text",
        )


class ConversationCreateSerializer(serializers.ModelSerializer):
    initial_message = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        write_only=True,
    )

    class Meta:
        model = Conversation
        fields = (
            "id",
            "pet_listing",
            "initial_message",
        )

    def create(self, validated_data):
        with transaction.atomic():
            initial_message = validated_data.pop("initial_message")
            conversation = Conversation.objects.create(**validated_data)
            Message.objects.create(
                conversation=conversation,
                sender=conversation.adopter,
                text=initial_message
            )

            return conversation


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = (
            "id",
            "pet_listing",
            "created_at"
        )


class ConversationRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = (
            "id",
            "pet_listing",
            "created_at"
        )
