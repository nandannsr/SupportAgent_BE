from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

class Message(models.Model):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("read", "Read"),
        ("failed", "Failed"),
    ]

    SENDER_CHOICES = [
        ("customer", "Customer"),
        ("agent", "Agent"),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="messages"
    )
    agent = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="sent")
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    whatsapp_message_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message from {self.sender_type} at {self.timestamp}"

class Notification(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="notifications"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Notification for {self.customer} at {self.timestamp}"
