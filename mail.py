import os
import re
import smtplib

from logger import get_logger

logger = get_logger(__name__)

GMAIL_SERVER = "smtp.gmail.com:587"

def fuzz_email(email: str) -> str:
    match = re.match(r"([^@]+)@([^@]+\.[^@]+)", email)
    if not match:
        return "***@***"

    user, domain = match.groups()
    tld = domain.split('.')[-1]
    return f"{user[0]}***@***.{tld}"


def send_email(subject: str, body: str, to: str):
    user = os.getenv("GOOGLE_EMAIL")
    password = os.getenv("GOOGLE_APP_PASSWORD")

    logger.info("Sending email with subject=%s", subject)
    server = smtplib.SMTP(GMAIL_SERVER)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.sendmail(user, to, f"Subject: {subject}\n\n{body}")
    server.quit()
    logger.info("Email sent successfully to %s", fuzz_email(to))
