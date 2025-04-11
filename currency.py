import os
from datetime import datetime, timedelta
from typing import Optional

import requests

from logger import get_logger
from mail import send_email

logger = get_logger(__name__)


def get_exchange_rate(source: str, target: str, date: Optional[str] = None) -> float:
    """
    Get the exchange rate between the source and target currencies.

    Returns:
        float: The exchange rate for the given date. If date is not provided, the current date is used.
    """
    APP_ID = os.getenv("OPENEXCHANGERATES_APP_ID")
    if not APP_ID:
        raise ValueError("OPENEXCHANGERATES_APP_ID is not set")

    if not date:
        day = "today"
        url = f"https://openexchangerates.org/api/latest.json?app_id={APP_ID}&base={source}"
    else:
        day = date
        url = f"https://openexchangerates.org/api/historical/{date}.json?app_id={APP_ID}&base={source}"

    logger.info("Fetching exchange rate for %s:%s on date=%s", source, target, day)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch exchange rate for {source}: {response.status_code} {response.text}")
    data = response.json()
    if "error" in data:
        raise ValueError(f"Error fetching exchange rate for {source}: {data}")

    rates = data["rates"]
    if not rates:
        raise ValueError("Missing rates in the response.")
    if target not in rates:
        raise ValueError(f"Target currency {target} not found in the response.")

    logger.info("Exchange rate between %s:%s is %s", source, target, rates[target])
    return rates[target]


def get_exchange_rates(source: str, target: str) -> tuple[float, float, float]:
    """
    Get the exchange rate between the source and target currencies for the given date.

    Returns:
        tuple[float, float, float]: The exchange rate for today, yesterday, and the difference in percentage.
    """
    today_rate = get_exchange_rate(source, target)
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_rate = get_exchange_rate(source, target, yesterday)
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
        today_rate, yesterday_rate, diff = get_exchange_rates(source, target)
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
