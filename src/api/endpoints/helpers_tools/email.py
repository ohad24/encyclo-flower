from envsmtp import EmailMessage, NameEmail
from pydantic import EmailStr
from core.config import get_settings
from models.user import UserVerificationTokenData, UserVerificationTokenDataExt
from db import get_db
from pymongo.database import Database
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
    user_id: str, email: EmailStr, base_url: str, db: Database = get_db()
):
    """
    Setup and send email verification token to user email.
    """

    # * create user email verification object
    user_verification = UserVerificationTokenData(
        user_id=user_id,
    )

    # * set email body
    body = f"""<div dir="rtl">
    ברכות על הצטרפותך לקהילת אנציקלופרח!

נא לאשר את כתובת המייל בקישור:
{os.getenv("APP_URL", str(base_url)[:-1])}/verify-email/{user_verification.token}

הגדרת צמחים מהנה!
<img style="max-width:200px;width:100%" src="https://storage.googleapis.com/ef-prod/logo.png" alt="logo">
</div>
"""

    # * store token in db
    db.email_verification_tokens.insert_one(user_verification.dict())

    # * send mail with token
    msg = EmailMessage(
        sender=NameEmail(settings.EMAIL_SENDER_NAME, settings.EMAIL_SENDER_ADDRESS),
        receipients=NameEmail("new user", email),
        subject="Email verification",
        body=body,
    )
    send_email(msg)


def setup_reset_password_email(
    user_id: str, email: EmailStr, base_url: str, db: Database = get_db()
):
    """
    Setup and send email verification token to user email.
    """

    # * create user email verification object
    user_verification = UserVerificationTokenDataExt(
        user_id=user_id,
    )

    # * set email body
    # TODO: setup a production email template
    body = f"""
    Hi,
    Please click the link below to reset your password:
    {base_url}{settings.API_PREFIX[1:]}/login/reset-password/{user_verification.token}

    The link will expire in 24 hours.

    Thanks,
    The {settings.APP_NAME} Team
    """

    # * store token in db
    db.reset_password_tokens.insert_one(user_verification.dict())

    # * send mail with token
    msg = EmailMessage(
        sender=settings.EMAIL_ADDRESS,
        receipients=email,
        subject="Reset password",
        body=body,
    )
    send_email(msg)
