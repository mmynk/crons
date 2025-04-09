import os

import requests

from logger import get_logger
from mail import send_email

logger = get_logger(__name__)


def get_exchange_rate(source: str, target: str) -> float:
    """
    Get the exchange rate between the source and target currencies.
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{source}"
    logger.info("Fetching exchange rate for %s", source)
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch exchange rate for {source}: {response.status_code} {response.text}")
    data = response.json()
    logger.info("Exchange rate fetched successfully.")
    if target not in data["conversion_rates"]:
        raise ValueError(f"Target currency {target} not found in the response.")
    rate = data["conversion_rates"][target]
    logger.info("Exchange rate %s:%s = %s", source, target, rate)
    return rate



def send_currency_alert(source: str, target: str, email: str):
    """
    Simply calculates the conversion rate between the source and target currencies
    and sends an alert email.

    Args:
        source (str): The source currency.
        target (str): The target currency.
    """
    logger.info("Sending exchange rate between %s:%s to %s", source, target, email)
    try:
        exchange_rate = get_exchange_rate(source, target)
    except ValueError as e:
        logger.error("Failed to get exchange rate: %s", e)
        return
    send_email(f"Currency Alert: {source} to {target}",
               f"The conversion rate between {source} and {target} is {exchange_rate}.", email)
    logger.info("Sent currency alert successfully.")
