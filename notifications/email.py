import threading

from django.conf import settings
from django.core import mail


class EmailThread(threading.Thread):
    def __init__(
        self, subject: str, plain_message: str, receiver: list, html_message: str
    ):
        threading.Thread.__init__(self)
        self.subject = subject
        self.plain_message = plain_message
        self.receiver = receiver
        self.html_message = html_message

    def run(self):
        mail.send_mail(
            subject=self.subject,
            message=self.plain_message,
            from_email=settings.FROM_EMAIL,
            recipient_list=self.receiver,
            html_message=self.html_message,
        )
