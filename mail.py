import os
import re
import smtplib

from logger import get_logger

logger = get_logger(__name__)

GMAIL_SERVER = "smtp.gmail.com:587"


def fuzz_email(email: str) -> str:
    """
    Validates and fuzzes the email address by replacing the user part with asterisks.
    If the email address does not follow the format of "user@domain.tld", then a ValueError is raised.

    Example:
    >>> fuzz_email("test@example.com")
    "t***@***.com"
    >>> fuzz_email("test@example.com.au")
    "t***@***.com.au"
    """
    match = re.match(r"([^@]+)@([^@]+\.[^@]+)", email)
    if not match:
        raise ValueError(f"Invalid email address: {email}")

    user, domain = match.groups()
    tld = domain.split('.')[-1]
    return f"{user[0]}***@***.{tld}"


def send_email(subject: str, body: str, to: str):
    user = os.getenv("GOOGLE_EMAIL")
    password = os.getenv("GOOGLE_APP_PASSWORD")

    # validate and fuzz email
    try:
        fuzzed_email = fuzz_email(to)
    except ValueError as e:
        logger.error("Invalid email address: %s", e)
        raise

    logger.info("Sending email with subject=%s to %s", subject, fuzzed_email)
    server = smtplib.SMTP(GMAIL_SERVER)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    try:
        server.sendmail(user, to, f"Subject: {subject}\n\n{body}")
    except smtplib.SMTPException as e:
        logger.error("Error sending email: %s", e)
    finally:
        server.quit()
    logger.info("Email sent successfully.")
