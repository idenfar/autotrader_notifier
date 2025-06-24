AutoTrader Notifier

This project provides a small Python script that checks an AutoTrader search page and notifies you of new listings via Gmail and Twilio SMS.

Running the Bot in the Cloud (GitHub Actions)

Everything happens in the cloud using GitHub Actions. You do not need to install Python or any other tools on your own computer. The steps below assume you are brand new to GitHub and have never configured secrets or workflows before.

1. Create a GitHub account  
   If you don't already have one, sign up at https://github.com.

2. Fork this repository  
   Click the "Fork" button at the top-right of the page to create a copy under your GitHub account.

3. Add repository secrets  
   In your fork, go to Settings → Secrets and variables → Actions. Use "New repository secret" to create each of the following entries. Enter the secret name exactly as shown and paste the value into the field:

   - SEARCH_URL – AutoTrader search results URL  
   - GMAIL_USER – Gmail address used to send emails  
   - GMAIL_APP_PASSWORD – Gmail app password  
   - TWILIO_SID – Twilio account SID  
   - TWILIO_TOKEN – Twilio auth token  
   - TWILIO_FROM – Twilio phone number to send from  
   - TWILIO_TO – Phone number to receive SMS messages

4. Schedule the workflow  
   In your fork, navigate to `.github/workflows/run_bot.yml` and click the pencil icon to edit. Replace the empty `cron:` line under `schedule:` with how often you want the bot to run. The value uses standard five-field cron syntax in UTC.  
   For example, `0 */2 * * *` will run every two hours. Commit the changes to save the schedule.

5. Run the bot manually (optional)  
   To trigger the bot manually at any time, go to the "Actions" tab in your fork, select "Run AutoTrader Bot", and click "Run workflow".

What Happens During a Run

When the workflow runs, it executes `autotrader_bot.py` in the GitHub Actions environment. If there are new listings on AutoTrader, the bot will:

- Send an email using Gmail
- Send an SMS using Twilio
- Record the listings in `seen_listings.json` to avoid duplicate alerts

The `seen_listings.json` file is:

- Uploaded as an artifact with each run (kept for 90 days)
- Used to track previously notified listings and prevent repeated alerts

You can download this file from any previous run in the "Actions" tab under the "Artifacts" section. You may also delete it from a run page at any time to reset the history.

Summary

This setup allows you to monitor new AutoTrader listings completely in the cloud — with no code to install or run on your own computer.
