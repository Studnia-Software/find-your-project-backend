from django.core.mail import EmailMessage
from django.conf import settings


class EmailService:
    def _send_message(self, message: EmailMessage) -> bool:
        pass

    def send_email(self, email: str, subject: str, to_address: str) -> EmailMessage:
        message = EmailMessage(
            subject=subject,
            body=email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_address],
        )

        sent = self._send_message(message)
        if sent:
            return message

        raise SystemError("Unable to send email")

