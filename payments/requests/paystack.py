import requests
from django.conf import settings
from . import params
from utils.exception import BadRequestException, ServerException


class PaystackClient:
    def __init__(self):
        self.base_url: str = settings.PAYSTACK_BASE_URL

        self.headers  = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        print(self.base_url)

        self.timeout = 30  # Timeout in 30 seconds

    def get(self, path=None, params=None):
        url = f"{self.base_url}{path}" if path is not None else f"{self.base_url}"
        response = requests.get(
            url, params=params, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def post(self, path=None, data=None, json=None):
        url = f"{self.base_url}{path}" if path is not None else f"{self.base_url}"

        try:

            response = requests.post(
                url, data=data, json=json, headers=self.headers, timeout=self.timeout
            )

            return response.json()

        except requests.exceptions.ConnectionError: # Raise if cant connect to paystack
            raise ServerException(
                message="Can not complete the transaction. Try again."
            )
        
        except requests.exceptions.RequestException as e : # Catch generic exceptions 
            raise BadRequestException(message=str(e))
        

    def initialize_transaction(self, initializer:params.IntializeTransaction):

        data = self.post(path="/transaction/initialize", data=initializer.model_dump_json())

        print(data)

        return data
