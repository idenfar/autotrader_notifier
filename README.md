# AutoTrader Notifier

This project provides a small Python script that checks an AutoTrader
search page and notifies you of new listings via Gmail and Twilio SMS.

Configuration values are read from environment variables or a `.env`
file. To create the `.env` file interactively run:

```bash
python autotrader_bot.py --setup
```

The following values are required:

- `SEARCH_URL` – AutoTrader search results URL
- `GMAIL_USER` – Gmail address used to send emails
- `GMAIL_APP_PASSWORD` – Gmail app password
- `TWILIO_SID` – Twilio account SID
- `TWILIO_TOKEN` – Twilio auth token
- `TWILIO_FROM` – Twilio phone number to send from
- `TWILIO_TO` – Phone number to receive SMS messages

`seen_listings.json` is used to keep track of listings that have already
been processed. The GitHub Actions workflow uploads this file as a build
artifact so state is preserved between runs.

To run locally after creating `.env`:

```bash
pip install -r requirements.txt
python autotrader_bot.py
```
