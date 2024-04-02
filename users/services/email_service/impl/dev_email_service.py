import os.path

from django.core.mail import EmailMessage
from os import path
import shutil

from users.services.email_service.email_service import EmailService
from django.conf import settings


class DevEmailService(EmailService):
    def __email_name(self, message: EmailMessage) -> path:
        i = 0
        name = str(message.to[0]) + "-" + message.subject + f"({i})"
        email_path = path.join(settings.EMAIL_BASE_DIR, name)
        while os.path.exists(email_path):
            i += 1
            name = str(message.to[0]) + "-" + message.subject + f"({i})"
            email_path = path.join(settings.EMAIL_BASE_DIR, name)

        return email_path

    def __new_email_file(self, message: EmailMessage):
        email_path = self.__email_name(message)

        with open(email_path, "a") as file:
            lines = [message.from_email, message.to[0], message.subject, message.body]
            lines = [line + "\n" for line in lines]
            file.writelines(lines)

    def _send_message(self, message: EmailMessage) -> bool:
        if not os.path.exists(settings.EMAIL_BASE_DIR):
            os.makedirs(settings.EMAIL_BASE_DIR)

        if len(os.listdir(settings.EMAIL_BASE_DIR)) != 0:
            shutil.rmtree(os.path.join(settings.EMAIL_BASE_DIR))
            os.makedirs(settings.EMAIL_BASE_DIR)

        self.__new_email_file(message)
        return True
