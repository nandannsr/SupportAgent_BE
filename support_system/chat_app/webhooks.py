import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView
from twilio.request_validator import RequestValidator

from .models import Customer, Message, Notification
from .serializers import MessageSerializer, NotificationSerializer


class TwilioWebhookView(APIView):
    """
    API view to handle incoming webhook requests from Twilio.

    This view validates that the request comes from Twilio, extracts message data,
    creates or updates the related Customer record, stores the incoming Message,
    creates a Notification for the new message, and broadcasts updates via WebSocket.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Process the incoming Twilio webhook POST request.

        The method performs the following steps:
        1. Validates the request using Twilio's RequestValidator.
        2. Extracts the sender's phone number, message body, and WhatsApp message SID.
        3. Retrieves or creates a Customer object based on the sender's phone number.
        4. Creates a Message instance for the incoming message.
        5. Generates a Notification indicating a new message.
        6. Broadcasts the new message and notification to their respective WebSocket groups.

        Args:
            request (Request): The HTTP request containing Twilio POST data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: A response with HTTP status 200 if successful, or HTTP status 403
                          if the request is invalid.
        """
        # Validate the request is from Twilio
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.headers.get("X-Twilio-Signature", ""),
        )

        if not request_valid and not settings.DEBUG:
            return HttpResponse(status=403)

        # Extract message data from the request
        from_number = request.POST.get("From", "").replace("whatsapp:", "")
        message_body = request.POST.get("Body", "")
        whatsapp_message_id = request.POST.get("MessageSid", "")

        # Retrieve or create the customer based on phone number
        customer, created = Customer.objects.get_or_create(phone_number=from_number)
        if created:
            customer.name = f"Customer {customer.id}"
            customer.save()

        # Create a new message instance
        message = Message.objects.create(
            customer=customer,
            content=message_body,
            sender_type="customer",
            status="received",
            whatsapp_message_id=whatsapp_message_id,
        )

        # Create a notification for the new message
        notification_content = f"New message from {customer.name}"
        notification = Notification.objects.create(
            customer=customer, content=notification_content
        )

        # Broadcast the new message and notification via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{customer.id}",
            {"type": "chat.message", "message": MessageSerializer(message).data},
        )
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "notification.message",
                "notification": NotificationSerializer(notification).data,
            },
        )

        return HttpResponse(status=200)
