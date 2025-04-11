from datetime import datetime, timedelta

import requests

from logger import get_logger
from mail import send_email

logger = get_logger(__name__)


def get_exchange_rate(source: str, target: str) -> tuple[float, float, float]:
    """
    Get the exchange rate between the source and target currencies.

    Returns:
        tuple[float, float, float]: The exchange rate today, yesterday, and the difference in percentage.
    """
    now = datetime.now()
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    today = now.strftime("%Y-%m-%d")
    url = f"https://api.frankfurter.app/{yesterday}..{today}?from={source}&to={target}"
    logger.info("Fetching exchange rate for %s", source)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch exchange rate for {source}: {response.status_code} {response.text}")
    data = response.json()
    logger.info("Exchange rate fetched successfully.")
    if not data["rates"] or not data["rates"][yesterday] or not data["rates"][today]:
        raise ValueError("Missing rates in the response.")

    rates = data["rates"]
    yesterday_rate = rates[yesterday]
    today_rate = rates[today]
    if not yesterday_rate[target] or not today_rate[target]:
        raise ValueError("Missing target rate in the response.")
    yesterday_rate = yesterday_rate[target]
    today_rate = today_rate[target]

    diff = (today_rate - yesterday_rate) / yesterday_rate
    return today_rate, yesterday_rate, diff


def send_currency_alert(source: str, target: str, email: str):
    """
    Simply calculates the conversion rate between the source and target currencies
    and sends an alert email.

    Args:
        source (str): The source currency.
        target (str): The target currency.
    """
    logger.info("Sending exchange rate between %s:%s", source, target)
    try:
        today_rate, yesterday_rate, diff = get_exchange_rate(source, target)
        logger.info("Exchange rate between %s:%s is today=%s, yesterday=%s, diff=%s", source, target, today_rate, yesterday_rate, diff)
    except ValueError as e:
        logger.error("Failed to get exchange rate: %s", e)
        return

    message = f"The conversion rate between {source} and {target} is {today_rate},"
    if diff < 0:
        message += " down"
    else:
        message += " up"
    message += f" {abs(diff):.2f}% from {yesterday_rate}."

    if email:
        try:
            subject = f"Currency Alert: {source} to {target}"
            body = message
            send_email(subject, body, email)
        except Exception as e:
            logger.error("Failed to send email: %s", e)
            return
    else:
        logger.info("No email provided, skipping email send.")
        logger.info(message)

    logger.info("Sent currency alert successfully.")
