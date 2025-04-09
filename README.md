# crons

This project is a collection of cron jobs to send alerts, run scripts, etc using GitHub Actions.

## Setup

The project uses environment variables for different services. Create a `.env` file in the root directory.

## Currency Alert

This cron job sends an email alert when the exchange rate between two currencies exceeds a certain threshold.

### Environment Variables

Add the following environment variables to your `.env` file:

- `EXCHANGE_RATE_API_KEY`: The API key for the [exchange rate service](https://www.exchangerate-api.com/).
- `GOOGLE_EMAIL`: The email address to send the alert from.
- `GOOGLE_APP_PASSWORD`: The app password for your [Google account](https://myaccount.google.com/apppasswords).

### Usage

```bash
python3 main.py currency -s USD -t INR -e your_email@gmail.com
```
