import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat messages.

    This consumer:
    - Accepts WebSocket connections for a specific customer chat room.
    - Joins the customer-specific group based on the customer_id from the URL.
    - Listens for messages from the WebSocket and broadcasts them to the group.
    - Sends messages from the group back to the connected WebSocket clients.
    """

    async def connect(self):
        """
        Handles a new WebSocket connection.

        Retrieves the customer_id from the URL, joins the corresponding
        chat group, and accepts the connection.
        """
        self.customer_id = self.scope["url_route"]["kwargs"]["customer_id"]
        self.room_group_name = f"chat_{self.customer_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.

        Leaves the chat group when the connection is closed.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handles incoming messages from the WebSocket.

        Parses the JSON message and sends it to the room group.
        """
        data = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": data}
        )

    async def chat_message(self, event):
        """
        Receives messages from the room group.

        Forwards the message to the WebSocket client.
        """
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time notifications.

    This consumer:
    - Establishes a WebSocket connection for general notifications.
    - Joins a notifications group to receive broadcasted notifications.
    - Allows receiving notifications from clients and broadcasts them to the group.
    - Sends notifications from the group back to the connected WebSocket clients.
    """

    async def connect(self):
        """
        Handles a new WebSocket connection for notifications.

        Joins the global notifications group and accepts the connection.
        """
        self.room_group_name = "notifications"

        # Join notification group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection for notifications.

        Leaves the notifications group when the connection is closed.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Handles incoming notifications from the WebSocket.

        Parses the JSON notification and sends it to the notifications group.
        """
        data = json.loads(text_data)

        # Send notification to notification group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "notification.message", "notification": data}
        )

    async def notification_message(self, event):
        """
        Receives notifications from the notifications group.

        Forwards the notification to the WebSocket client.
        """
        notification = event["notification"]

        # Send notification to WebSocket
        await self.send(text_data=json.dumps(notification))
