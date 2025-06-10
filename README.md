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

If you only want to run the notifier in the cloud with GitHub Actions,
you can skip the installation steps above and go straight to the next
section. In that case you will provide the same values as GitHub secrets
instead of creating a `.env` file.

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

## Automate in the cloud (GitHub Actions)

GitHub Actions can run the notifier for you on a schedule. Follow these
steps entirely in your web browser:

1. **Fork this repository** – Click the **Fork** button at the top of the
   page to create a copy under your GitHub account.
2. Open your fork's **Settings → Secrets and variables → Actions** page.
   Add a new secret for each of the values you entered during local
   setup: `SEARCH_URL`, `GMAIL_USER`, `GMAIL_APP_PASSWORD`,
   `TWILIO_SID`, `TWILIO_TOKEN`, `TWILIO_FROM`, and `TWILIO_TO`.
3. Still in your fork, navigate to `.github/workflows/run_bot.yml` and
   click the pencil icon to edit the file. The line beginning with
   `cron:` controls how often the notifier runs. Change it if you want a
   different schedule, then choose **Commit changes**.
4. The workflow will now run automatically according to the schedule you
   set. To trigger it immediately, open the **Actions** tab, select
   **Run AutoTrader Bot**, and click **Run workflow**.

Each run uploads a `seen_listings.json` artifact so that previously
processed listings are remembered. You can delete this artifact from the
run page any time you want to reset the history.

