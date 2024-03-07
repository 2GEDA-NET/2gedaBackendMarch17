from decimal import Decimal

import requests
from django.conf import settings


class Paystack(object):
    """Paystack class for API"""

    base_url = settings.PAYSTACK_BASE_URL
    kobo = 100
    network_error = {
        "message": "Can not complete the transaction. Try again.",
        "status": False,
    }
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "context_type": "application/json",
    }

    @classmethod
    def initialize(cls, amount, email, **params):
        url = f"{cls.base_url}/transaction/initialize"
        amount_str = f"{amount * cls.kobo}"
        # callback_url =
        data = {"amount": amount_str, "email": email}
        data.update(params)

        try:
            response = requests.post(url=url, data=data, headers=cls.headers)
        except requests.exceptions.ConnectionError:
            return False, cls.network_error
        else:
            return True, response.json()

    @classmethod
    def verify(cls, reference):
        url = f"{cls.base_url}/transaction/verify/{reference}"
        try:
            response = requests.get(url=url, headers=cls.headers)
        except requests.exceptions.ConnectionError:
            return False, cls.network_error
        else:
            return True, response.json()
