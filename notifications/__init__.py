from django.template.loader import render_to_string

# from user.account.models import Notification

from .email import EmailThread


# def send_notification(recipient, sender, message):
#     notification = Notification(recipient=recipient, sender=sender, message=message)
#     notification.save()


def send_verification_code(user: object, verification_type: str) -> None:
    """Send Email notification to users."""
    subject = ""
    template = ""

    if verification_type == "account_verification":
        subject = "2geda Account Verification Code"
        template = ""

    if verification_type == "password_verification":
        subject = "Forget Password Verification Code"
        template = ""

    EmailThread(
        subject=subject,
        plain_message="Hi %s, Your verification code is %s."
        % (
            user.username,
            user.one_time_password.order_by("-created_at").first().otp,
        ),
        receiver=[user.email],
        html_message=(
            render_to_string(template, context={"user": user}) if template else None
        ),
    ).run()
