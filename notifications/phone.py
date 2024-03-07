from django.conf import settings


TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = settings.TWILIO_PHONE_NUMBER
# Send the OTP to the user's phone number via Twilio


# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
# message = client.messages.create(
#     body=f"Hi, {user.username}, Your OTP code is: {otp_code}",
#     from_=TWILIO_PHONE_NUMBER,
#     to=phone_number,  # Replace with the user's phone_number field
# )
