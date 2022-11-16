import os
import time
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from config import settings
import pathlib
import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


broker = RabbitmqBroker(url=settings.BROKER_URL)
dramatiq.set_broker(broker)


@dramatiq.actor
def task_test():
    time.sleep(5)
    print(" [*] Test task executed succefully!")


@dramatiq.actor
def send_email(
    subject: str, html_message: str, receiver_list: list, filename: str = None
):
    total = 0
    for total_sent, receiver_email in enumerate(receiver_list, 1):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.EMAIL_HOST_FROM
        msg["To"] = receiver_email
        part = MIMEText(html_message, "html")
        msg.attach(part)
        if filename:
            file_path = settings.MEDIA_ROOT.joinpath(filename)
            if pathlib.Path(file_path).exists():
                with open(file_path, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment", filename=filename)
                msg.attach(part)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            settings.EMAIL_HOST, settings.EMAIL_PORT, context=context
        ) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_FROM, receiver_email, msg.as_string())
        total = total_sent
    print(f" [*] Total of {total} email(s) succefully sent!")
