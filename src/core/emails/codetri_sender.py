from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import localtime, make_msgid
from smtplib import SMTP

from src.core.config import load_app_config


__all__ = [
    "send_emails_codetri"
]


def rewrite_email_structure(msg: dict) -> EmailMessage:
    # Split the "To" address into the separate parts
    addr_to = msg["To"][0]["Email"].split("@")

    # Instance the email message and set any headers we need
    em = EmailMessage()
    em["Message-ID"] = make_msgid(domain="codetri.net")
    em["Date"] = localtime()

    # Set all of the message details
    em["subject"] = msg["Subject"]
    em["from"] = Address("#vss365 today", "noreply", "codetri.net")
    em["to"] = Address("#vss365 today Subscriber", addr_to[0], addr_to[1])
    em.set_content(msg["HTMLPart"], subtype="html")
    return em


def send_emails(msgs: list):
    # Rewrite the emails to be in the correct format
    msgs = [
        rewrite_email_structure(msg)
        for msg in msgs
    ]

    # Connect to the local running SMTP server
    CONFIG = load_app_config()
    with SMTP(
        CONFIG["SMTP_SERVER_ADDRESS"],
        CONFIG["SMTP_SERVER_PORT"]
    ) as server:
        server.ehlo_or_helo_if_needed()
        server.set_debuglevel(1)  # TODO Remove this line

        # Send each message
        # TODO There needs to be some form of logging in place
        # for tracking sucessful/failed messages, if at all possible
        for msg in msgs:
            server.send_message(msg)
