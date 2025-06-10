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

