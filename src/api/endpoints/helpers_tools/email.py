from envsmtp import EmailMessage
from pydantic import EmailStr
from core.config import get_settings
from uuid import uuid4
from models.user import UserEmailVerification
from db import get_db
from pymongo import MongoClient
import os
import logging

settings = get_settings()


def send_email(msg: EmailMessage):
    if os.environ.get("SMTP_USER") and os.environ.get("SMTP_PASS"):
        msg.smtp_send()
    else:
        logging.warning(
            "SMTP_USER and SMTP_PASS not found in environment variables. Email not sent."
        )


def setup_email_verification(
    user_id: str, email: EmailStr, base_url: str, db: MongoClient = get_db()
):
    """
    Setup and send email verification token to user email.
    """

    # * generate token
    email_verification_token = uuid4().hex

    # * set email body
    # TODO: setup a production email template
    body = f"""
    Hi,
    Please click the link below to verify your email address:
    {base_url}{settings.API_PREFIX[1:]}/users/verify-email/{email_verification_token}

    The link will expire in 48 hours.

    Thanks,
    The {settings.APP_NAME} Team
    """

    # * create user email verification object
    email_verification = UserEmailVerification(
        user_id=user_id,
        token=email_verification_token,
    )

    # * store token in db
    db.email_verification_tokens.insert_one(email_verification.dict())

    # * send mail with token
    msg = EmailMessage(
        sender=settings.EMAIL_ADDRESS,
        receipients=email,
        subject="Email verification",
        body=body,
    )
    send_email(msg)
