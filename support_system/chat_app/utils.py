from django.conf import settings
from twilio.rest import Client


def get_twilio_client():
    # Initialize Twilio client
    twilio_account_sid = settings.TWILIO_ACCOUNT_SID
    twilio_auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(twilio_account_sid, twilio_auth_token)

    return client
