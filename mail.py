import os
import smtplib

from logger import get_logger

logger = get_logger(__name__)

GMAIL_SERVER = "smtp.gmail.com:587"

def send_email(subject: str, body: str, to: str):
    user = os.getenv("GOOGLE_EMAIL")
    password = os.getenv("GOOGLE_APP_PASSWORD")

    logger.info("Sending email to %s: subject=%s", to, subject)
    server = smtplib.SMTP(GMAIL_SERVER)
    server.ehlo()
    server.starttls()
    server.login(user, password)
    server.sendmail(user, to, f"Subject: {subject}\n\n{body}")
    server.quit()
    logger.info("Email sent successfully.")
