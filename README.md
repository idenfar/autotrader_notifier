# AutoTrader Notifier

This project provides a small Python script that checks an AutoTrader
search page and notifies you of new listings via Gmail and Twilio SMS.

## Step-by-step setup

The instructions below walk through the entire process as if you have
never used Python before. Follow them in order and you will have a working notifier on your own computer.

1. **Install Python** – Download Python 3.10 or later from
   [python.org](https://www.python.org/downloads/). During installation
   make sure to tick the option that adds Python to your `PATH`.
2. **Download the project** – Click the green **Code** button on this
   page and choose **Download ZIP**. Once downloaded, extract the ZIP
   file to a folder you can easily find, for example your Desktop.
3. **Open a terminal** – On Windows you can use *Command Prompt*. On
   macOS or Linux open the *Terminal* application. Use the `cd` command
   to move into the folder you extracted, e.g.:

   ```bash
   cd path/to/autotrader_notifier
   ```
4. **Install required Python packages** – Run:

   ```bash
   pip install -r requirements.txt
   ```
5. **Create configuration file** – Run the setup command and answer the
   prompts. A `.env` file will be written with your answers.

   ```bash
   python autotrader_bot.py --setup
   ```
   The script will ask for the values listed in the **Required information** section below.
6. **Run the notifier** – After the `.env` file is created start the
   script:

   ```bash
   python autotrader_bot.py
   ```
   New listings will trigger an email and SMS and will be recorded in
`seen_listings.json` so you are not alerted twice.

### Required information

During setup you will be prompted for:
- `SEARCH_URL` – AutoTrader search results URL
- `GMAIL_USER` – Gmail address used to send emails
- `GMAIL_APP_PASSWORD` – Gmail app password
- `TWILIO_SID` – Twilio account SID
- `TWILIO_TOKEN` – Twilio auth token
- `TWILIO_FROM` – Twilio phone number to send from
- `TWILIO_TO` – Phone number to receive SMS messages

The GitHub Actions workflow uploads the `seen_listings.json` file as a
build artifact so state is preserved between runs.

To run the notifier again later just run:

```bash
python autotrader_bot.py
```

## Run in the cloud (GitHub Actions)

You can automate the notifier in the cloud using GitHub Actions. This
lets it run on a schedule without your computer needing to be on.

1. **Fork this repository** to your own GitHub account and clone the
   fork locally if you want to make changes.
2. In your fork on GitHub open **Settings → Secrets and variables →
   Actions** and create secrets for each value from the **Required
   information** list above. Use the same names (`SEARCH_URL`,
   `GMAIL_USER`, `GMAIL_APP_PASSWORD`, and so on).
3. Push your fork to GitHub. The included workflow file
   `.github/workflows/run_bot.yml` will run automatically every
   30&nbsp;minutes.
4. To change how often it runs, edit the `cron:` line in that workflow
   file. For example `cron: '0 * * * *'` would run hourly. Commit the
   change and push it to GitHub.
5. You can also trigger a run manually from the **Actions** tab by
   selecting the workflow and clicking **Run workflow**.

The `seen_listings.json` artifact is saved after each run so that
previously processed listings are remembered. If you ever want to start
fresh simply delete the artifact from the run page.

