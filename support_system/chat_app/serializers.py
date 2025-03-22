from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Customer, Message, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'phone_number', 'name', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    agent_details = UserSerializer(source='agent', read_only=True)
    customer_details = CustomerSerializer(source='customer', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'customer', 'customer_details', 'agent', 'agent_details',
            'content', 'timestamp', 'status', 'sender_type', 'whatsapp_message_id'
        ]
        read_only_fields = ['timestamp', 'whatsapp_message_id']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"