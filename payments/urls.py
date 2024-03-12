from django.urls import path
from . import api


urlpatterns = [
    path("webhook/", api.PaystackWebhookView.as_view(), name="paystack-webhook"),
]
