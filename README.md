# AutoTrader Notifier

This project provides a small Python script that checks an AutoTrader
search page and notifies you of new listings via Gmail and Twilio SMS.

## Running the bot in GitHub

Everything happens in the cloud using GitHub Actions. You do not need to
install Python or any other tools on your own computer. The steps below
assume you are brand new to GitHub and have never configured secrets or
workflows before.

1. **Create a GitHub account** – If you don't already have one, sign up
   at [github.com](https://github.com). All of the remaining steps happen
   in your GitHub account.
2. **Fork this repository** – At the top‑right of the page click the
   **Fork** button. This makes your own copy of the code where you can
   save settings.
3. **Add repository secrets** – Secrets store private information (like
   passwords) that workflows can read. In your new fork:
   1. Click **Settings**.
   2. Choose **Secrets and variables → Actions** from the left menu.
   3. Use **New repository secret** to create each item listed in the
      **Required information** section below. Enter the secret name exactly
      as shown and paste the value into the field.
4. **Schedule the workflow** – Open `.github/workflows/run_bot.yml` in
   your fork and click the pencil icon to edit. Replace the empty
   `cron:` line under `schedule:` with how often you want the bot to run.
   The value uses standard five‑field [cron syntax](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows#schedule)
   in UTC. For example `0 */2 * * *` runs every two hours. Commit this
   change to save the schedule.
5. **Run the bot manually** – Navigate to the **Actions** tab in your
   repository and select **Run AutoTrader Bot**. Click **Run workflow** to
   start a run immediately. Future runs will happen automatically using
   the schedule you configured.

When the workflow runs, it executes `autotrader_bot.py` in the GitHub
Actions environment. New listings trigger an email and SMS. The file
`seen_listings.json` is saved as an artifact so the bot remembers which
listings it has already notified you about.

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

