from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from conversations.models import Conversation, Message
from conversations.serializers import ConversationListSerializer, ConversationRetrieveSerializer, \
    ConversationCreateSerializer, MessageCreateSerializer, MessageListSerializer


class ConversationViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Conversation.objects.all()
    serializer_class = ConversationListSerializer
    permission_classes = [IsAuthenticated,]


    def get_serializer_class(self):
        if self.action == "create":
            return ConversationCreateSerializer
        elif self.action == "retrieve":
            return ConversationRetrieveSerializer

        elif self.action == "messages":
            if self.request.method == "POST":
                return MessageCreateSerializer
            return MessageListSerializer

        return ConversationListSerializer

    @action(
        methods=["GET", "POST"],
        detail=True,
    )
    def messages(self, request, pk=None):
        conversation = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                conversation=conversation,
                sender=self.request.user
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        else:
            queryset = Message.objects.filter(
                conversation=conversation
            )
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(
                    page, many=True
                )
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(
                queryset, many=True
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )


    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(
            Q(adopter_id=self.request.user.id)
            | Q(pet_listing__author_id=self.request.user.id)
        )

        return queryset

    def perform_create(self, serializer):
        serializer.save(adopter=self.request.user)

    def create(self, request, *args, **kwargs):
        pet_listing_id = request.data.get("pet_listing")
        adopter_id = request.user.id

        conversation = Conversation.objects.filter(
            pet_listing_id=pet_listing_id,
            adopter_id=adopter_id
        ).first()

        if conversation:
            serializer = self.get_serializer(
                conversation
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(
                data=request.data
            )

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer=serializer)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
