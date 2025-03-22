from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Message, Notification
from .serializers import (CustomerSerializer, MessageSerializer,
                          NotificationSerializer)
from .utils import get_twilio_client


class CustomerView(APIView):
    """
    API view to retrieve customer information.

    GET:
    - If a 'customer_id' query parameter is provided, returns the specified customer.
    - Otherwise, returns the full list of customers.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve customer data based on the presence of a 'customer_id' query parameter.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: Serialized customer data.
        """
        customer_id = request.query_params.get("customer_id")
        if customer_id:
            customer = get_object_or_404(Customer, pk=customer_id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        else:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data)


class MessageView(APIView):
    """
    API view to handle retrieval and creation of messages.

    GET:
    - Returns all messages for the provided 'customer_id' query parameter.
    - If 'customer_id' is missing, returns an error.

    POST:
    - Creates a new message for a given customer and sends it via Twilio WhatsApp.
    - Expects 'customer_id' and 'content' in the request data.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all messages for a specified customer.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: Serialized message data if customer_id is provided; error response otherwise.
        """
        customer_id = request.query_params.get("customer_id")
        if not customer_id:
            return Response(
                {"error": "customer_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        messages = Message.objects.filter(customer_id=customer_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new message and send it using Twilio WhatsApp API.

        Expects:
            - customer_id: The ID of the customer.
            - content: The message content.

        Returns:
            Response: Serialized message data with status 201 on success; error response otherwise.
        """
        customer_id = request.data.get("customer_id")
        content = request.data.get("content")

        if not customer_id or not content:
            return Response(
                {"error": "customer_id and content are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = get_object_or_404(Customer, pk=customer_id)

        # Create message in the database
        message = Message.objects.create(
            customer=customer,
            agent=request.user,
            content=content,
            sender_type="agent",
            status="sent",
        )

        try:
            client = get_twilio_client()
            twilio_whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
            twilio_message = client.messages.create(
                body=content,
                from_=f"whatsapp:{twilio_whatsapp_number}",
                to=f"whatsapp:{customer.phone_number}",
            )
            # Update message with WhatsApp message ID
            message.whatsapp_message_id = twilio_message.sid
            message.save()

            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            message.status = "failed"
            message.save()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NotificationView(APIView):
    """
    API view to manage notifications.

    GET:
    - Returns only unread notifications.

    POST:
    - Marks a notification as read based on the provided notification id in the request data.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all unread notifications.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: Serialized unread notification data.
        """
        unread_notifications = Notification.objects.filter(is_read=False)
        serializer = NotificationSerializer(unread_notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Mark a notification as read.

        Expects:
            - id: The notification ID.

        Returns:
            Response: Serialized notification data with updated status on success; error response otherwise.
        """
        notification_id = request.data.get("id")
        if not notification_id:
            return Response(
                {"error": "Notification id not provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        notification = get_object_or_404(Notification, id=notification_id)
        notification.is_read = True
        notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
