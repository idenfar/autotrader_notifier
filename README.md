AutoTrader Notifier

This project provides a small Python script that checks an AutoTrader search page and notifies you of new listings via Gmail and Twilio SMS.

Running the Bot in the Cloud (GitHub Actions)

Everything happens in the cloud using GitHub Actions. You do not need to install Python or any other tools on your own computer. The steps below assume you are brand new to GitHub and have never configured secrets or workflows before.

1. Create a GitHub account  
   If you don't already have one, sign up at https://github.com.

2. Fork this repository  
   Click the "Fork" button at the top-right of the page to create a copy under your GitHub account.

3. Add repository secrets
   In your fork, go to Settings → Secrets and variables → Actions. Use "New repository secret" to create each of the following entries. Enter the secret name exactly as shown and paste the value into the field. These secrets keep your credentials out of version control. **Do not commit real passwords, tokens, or `.env` files to the repository.**

   - SEARCH_URL – AutoTrader search results URL  
   - GMAIL_USER – Gmail address used to send emails  
   - GMAIL_APP_PASSWORD – Gmail app password  
   - TWILIO_SID – Twilio account SID  
   - TWILIO_TOKEN – Twilio auth token  
   - TWILIO_FROM – Twilio phone number to send from  
   - TWILIO_TO – Phone number to receive SMS messages

4. Schedule the workflow
   The workflow is configured to run every 15 minutes by default. If you prefer a
   different interval, edit the `cron:` line in `.github/workflows/run_bot.yml`.
   The value uses standard five-field cron syntax in UTC.

5. Run the bot manually (optional)  
   To trigger the bot manually at any time, go to the "Actions" tab in your fork, select "Run AutoTrader Bot", and click "Run workflow".

What Happens During a Run

When the workflow runs, it executes `autotrader_bot.py` in the GitHub Actions environment. If there are new listings on AutoTrader, the bot will:

- Send an email using Gmail
- Send an SMS using Twilio *(SMS may incur charges depending on your Twilio account)*
- Record the listings in `seen_listings.json` to avoid duplicate alerts

The `seen_listings.json` file and archived listing pages are committed back to
the repository after each run. This history allows you to track all listings that
triggered a notification.

Summary

This setup allows you to monitor new AutoTrader listings completely in the cloud — with no code to install or run on your own computer.
