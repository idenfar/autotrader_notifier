🚗 AutoTrader Notifier

A Python-based GitHub Actions bot that monitors an AutoTrader.ca search page and notifies you of new listings via Gmail and Twilio SMS — all automatically in the cloud.

===============================================================================

✨ Features

- Fully cloud-based: runs on GitHub Actions
- Sends instant email and SMS notifications for new listings
- Remembers previously seen listings to prevent duplicates
- Archives full HTML and images of each listing
- Commits historical data to your repository for tracking

===============================================================================

☁️ Cloud-Only Setup (No Local Installation Needed)

You don’t need to install Python or run anything on your computer. The bot runs entirely in the GitHub Actions environment.

-------------------------------------------------------------------------------

🔧 Step-by-Step Instructions

1. Create a GitHub Account  
   Sign up at https://github.com if you don’t already have an account.

2. Fork This Repository  
   Click the 'Fork' button at the top-right to create your own copy of this repository.
   Your fork will be public by default. If you prefer to keep it private,
   go to your forked repository's Settings → General and change the visibility to **Private**.

3. Add Repository Secrets  
   Go to your forked repo’s Settings → Secrets and variables → Actions.  
   Click 'New repository secret' for each of the following:

   - `SEARCH_URL`         – AutoTrader search results URL  
   - `GMAIL_USER`         – Gmail address used to send emails  
   - `GMAIL_APP_PASSWORD` – Gmail app password (use App Passwords, not your login password)  
   - `TWILIO_SID`         – Twilio Account SID  
   - `TWILIO_TOKEN`       – Twilio Auth Token  
   - `TWILIO_FROM`        – Twilio phone number to send from  
   - `TWILIO_TO`          – Your phone number to receive SMS
   Before using Gmail, enable 2-Step Verification and create an App Password for "Mail". Use that value for `GMAIL_APP_PASSWORD`.

   ⚠️ Never commit passwords or .env files to the repository. Use secrets only.

4. Schedule the Workflow  
   Open `.github/workflows/run_bot.yml` and edit the `cron:` line to control how often the bot runs (default is every 15 minutes).

   Example (every 15 minutes UTC):
   schedule:
     - cron: '*/15 * * * *'

   Visit https://crontab.guru for custom schedule formatting.

5. Run It Manually (Optional)  
   Go to the 'Actions' tab → select 'Run AutoTrader Bot' → click 'Run workflow'.

===============================================================================

🏃 What Happens During a Run

- Executes `autotrader_bot.py`  
- Detects new listings from your `SEARCH_URL`  
- Sends:
  - 📧 Email via Gmail  
  - 📱 SMS via Twilio (charges may apply)  
- Records listing IDs in `seen_listings.json`  
- Archives each listing under `archives/`, including:
  - `page.html` – full listing HTML  
  - `image_*.jpg` – all listing images  
  - `metadata.json` – title, URL, and file references

All of this is committed back to your repository automatically.

===============================================================================

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

===============================================================================

🙋‍♂️ Questions or Contributions?

Feel free to open an issue or submit a pull request. Contributions are welcome!
