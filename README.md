# AutoTrader Bot

A Python-based GitHub Actions bot that monitors an AutoTrader.ca search page and notifies you of new listings via Gmail and Twilio SMS — all automatically in the cloud.

==============================================================================

✨ Features

- Fully cloud-based: runs on GitHub Actions
- Sends instant email and SMS notifications for new listings
- Remembers previously seen listings to prevent duplicates
- Archives full HTML and images of each listing
- Commits historical data to your repository for tracking

==============================================================================

☁️ Cloud-Only Setup (No Local Installation Needed)

You don’t need to install Python or run anything on your computer. The bot runs entirely in the GitHub Actions environment.

------------------------------------------------------------------------------

🔧 Step-by-Step Instructions

1. Create a GitHub Account
   Sign up at https://github.com if you don’t already have an account.

2. Fork This Repository
   Click the 'Fork' button at the top-right to create your own copy of this repository.  
   Your fork will be public by default. If you prefer to keep it private,  
   go to your forked repository's Settings → General and change the visibility to **Private**.

3. Enable GitHub Actions on Your Fork
   When you first open the **Actions** tab, GitHub shows a notice:

   *Workflows aren’t being run on this forked repository*

   Because this repository contained workflow files when it was forked,
   they’re disabled until you explicitly enable them. Click **"I understand my workflows, go ahead and enable them"**.

   After enabling, a workflow named **Run Autotrader Bot** appears in the sidebar with a **Disabled** badge. Select it and click the **Enable workflow** button in the banner that states *This scheduled workflow is disabled because scheduled workflows are disabled by default in forks.*

4. Turn On Gmail 2-Step Verification
   1. Visit <https://myaccount.google.com/security>.  
   2. Under **How you sign in to Google**, click **2-Step Verification**.  
   3. Follow the prompts (confirm your password, add a phone, etc.) until it shows **On**.

5. Create a Gmail App Password
   1. Back on the **Security** page, choose **App passwords** (sign in again if asked). Direct link: <https://myaccount.google.com/apppasswords>  
   2. Select **Mail** for the app and name it "AutoTrader Bot".  
   3. Click **Generate**.  
   4. Copy the 16-character password Google displays (omit the spaces).  
   5. You’ll use this code as `GMAIL_APP_PASSWORD` in the next step.

6. Add Repository Secrets
   Go to your forked repo’s Settings → Secrets and variables → Actions.  
   Click 'New repository secret' for each of the following:

   - `SEARCH_URL`         – AutoTrader search results URL  
   - `GMAIL_USER`         – Gmail address used to send emails  
   - `GMAIL_APP_PASSWORD` – Gmail app password (use App Passwords, not your login password)  
   - `TWILIO_SID`         – Twilio Account SID  
   - `TWILIO_TOKEN`       – Twilio Auth Token  
   - `TWILIO_FROM`        – Twilio phone number to send from  
   - `TWILIO_TO`          – Your phone number to receive SMS

   ⚠️ Never commit passwords or .env files to the repository. Use secrets only.
   Your `GMAIL_USER` should be the same Gmail account used in steps 4 and 5.
   You can send notifications to this address or any other—no additional Gmail  
   settings are required once the app password is configured.

7. Schedule the Workflow
   Open `.github/workflows/run_bot.yml` and edit the `cron:` line to control how often the bot runs (default is every 15 minutes).

   Example (every 15 minutes UTC):
   schedule:
     - cron: '*/15 * * * *'

Visit https://crontab.guru for custom schedule formatting.

8. Run It Manually (Optional)
   In the **Run Autotrader Bot** workflow page, click **Run workflow**.
   Leave **Branch: main** selected and hit the green **Run workflow** button. GitHub will display *Workflow run was successfully requested* and you can click into the run to watch it live.

==============================================================================

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

==============================================================================

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

