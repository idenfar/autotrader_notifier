# AutoTrader Notifier

This project provides a small Python script that checks an AutoTrader
search page and notifies you of new listings via Gmail and Twilio SMS.

## Setup using GitHub Actions

The notifier can run entirely in the cloud with no local Python
installation. Follow these steps to configure the workflow:

1. **Fork the repository** – Use the **Fork** button on GitHub to create
   your own copy.
2. **Add repository secrets** – In your fork open
   *Settings → Secrets → Actions* and create secrets for the values listed
   in the **Required information** section below. The workflow will export
   them as environment variables when it runs.
3. **Configure the schedule** – The workflow file is located at
   `.github/workflows/run_bot.yml`. Edit the `cron` expression under the
   `schedule` key to control how often the bot runs, or trigger it
   manually using the *Run workflow* button.
4. **Start the workflow** – Once your secrets are saved, the next
   scheduled run (or a manual run) will execute `autotrader_bot.py` in the
   GitHub Actions environment. New listings trigger an email and SMS and
   are recorded in `seen_listings.json` which is uploaded as a build
   artifact so state is preserved between runs.

### Required information

Add these secrets to your repository:
- `SEARCH_URL` – AutoTrader search results URL
- `GMAIL_USER` – Gmail address used to send emails
- `GMAIL_APP_PASSWORD` – Gmail app password
- `TWILIO_SID` – Twilio account SID
- `TWILIO_TOKEN` – Twilio auth token
- `TWILIO_FROM` – Twilio phone number to send from
- `TWILIO_TO` – Phone number to receive SMS messages

The GitHub Actions workflow uploads the `seen_listings.json` file as a
build artifact so state is preserved between runs.

