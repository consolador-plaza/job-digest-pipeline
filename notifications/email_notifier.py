import smtplib

import os

from email.message import EmailMessage

from dotenv import load_dotenv

from pathlib import Path

ROOT = (

    Path(__file__)

    .resolve()

    .parent

    .parent
)


load_dotenv(

    ROOT / ".env"
)


class EmailNotifier:


    def __init__(

        self
    ):


        self.sender = os.getenv(
            "NOTIFY_EMAIL"
        )


        self.password = os.getenv(
            "NOTIFY_PASSWORD"
        )


        self.receiver = os.getenv(
            "NOTIFY_TO"
        )


    def send(

        self,

        subject,

        body
    ):


        msg = EmailMessage()


        msg["Subject"] = subject

        msg["From"] = self.sender

        msg["To"] = self.receiver


        msg.set_content(
            body
        )


        with smtplib.SMTP(

            "smtp.gmail.com",

            587
        ) as s:


            s.starttls()


            s.login(

                self.sender,

                self.password
            )


            s.send_message(
                msg
            )