from django.urls import include, path

from .views import *
from .webhooks import *

urlpatterns = [
    path("customers/", CustomerView.as_view(), name="customer-view"),
    path("messages/", MessageView.as_view(), name="message-view"),
    path("notifications/", NotificationView.as_view(), name="notifications"),
    path("webhooks/twilio/", TwilioWebhookView.as_view(), name="twilio-webhook"),
]
