# Math Lead Sniper - Setup Instructions

This document provides step-by-step instructions for setting up and running the Math Lead Sniper.

## Prerequisites

- Python 3.8 or higher
- Internet connection
- Accounts for: Reddit, Google AI Studio, and Discord

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## API Keys and Credentials Setup

### 2. Get Your Google AI Studio API Key (Gemini)

The Math Lead Sniper uses Google's Gemini 1.5 Flash model for AI-powered lead qualification.

**Step-by-Step Instructions:**

1. **Go to Google AI Studio**
   - Visit: https://aistudio.google.com/

2. **Sign in with your Google Account**
   - Use any Google account (Gmail, Workspace, etc.)

3. **Get Your API Key**
   - Click on **"Get API key"** in the left sidebar
   - Click **"Create API key"**
   - Choose **"Create API key in new project"** (or select an existing Google Cloud project)
   - Copy the API key that appears

4. **Important Notes:**
   - Keep this key secret and never commit it to version control
   - Gemini 1.5 Flash has a generous free tier (15 requests per minute)
   - For pricing details: https://ai.google.dev/pricing

### 3. Get Your Reddit Client ID and Secret

The Math Lead Sniper monitors Reddit for math tutoring leads.

**Step-by-Step Instructions:**

1. **Go to Reddit App Preferences**
   - Visit: https://www.reddit.com/prefs/apps
   - Sign in to your Reddit account

2. **Create a New Application**
   - Scroll to the bottom and click **"create another app..."** or **"are you a developer? create an app..."**

3. **Fill Out the Form:**
   - **Name:** `Math Lead Sniper` (or any name you prefer)
   - **App type:** Select **"script"**
   - **Description:** `Monitors math subreddits for tutoring leads` (optional)
   - **About URL:** Leave blank or use your website
   - **Redirect URI:** Enter `http://localhost:8080` (required but not used)
   - Click **"create app"**

4. **Get Your Credentials:**
   - After creating the app, you'll see:
     - **Client ID:** The string under "personal use script" (14 characters)
     - **Client Secret:** The string next to "secret" (27 characters)
   - Copy both values

5. **Important Notes:**
   - Reddit has rate limits: 60 requests per minute
   - Use a descriptive User Agent (already configured in the script)
   - Don't share your client secret

### 4. Get Your Discord Webhook URL

The Math Lead Sniper sends notifications to Discord via webhooks.

**Step-by-Step Instructions:**

1. **Open Discord and Select Your Server**
   - Open Discord (desktop app or web)
   - Select the server where you want to receive notifications

2. **Create a Channel (Optional)**
   - Right-click on your server name → **"Create Channel"**
   - Name it `math-leads` or similar
   - Set permissions as desired

3. **Create a Webhook:**
   - Right-click on the channel → **"Edit Channel"**
   - Click **"Integrations"** in the left sidebar
   - Click **"Create Webhook"** or **"Webhooks"** → **"New Webhook"**

4. **Configure the Webhook:**
   - **Name:** `Math Lead Sniper` (this will appear as the bot name)
   - **Channel:** Select your desired channel
   - **Icon:** Upload an icon (optional)

5. **Copy the Webhook URL:**
   - Click **"Copy Webhook URL"**
   - The URL will look like: `https://discord.com/api/webhooks/123456789/abcdefg...`

6. **Save Changes:**
   - Click **"Save Changes"**

7. **Important Notes:**
   - Keep the webhook URL secret (anyone with it can post to your channel)
   - You can edit or delete the webhook anytime from the same menu

### 5. Set Up Google Alerts RSS (Optional)

Google Alerts can monitor the web for specific keywords and provide RSS feeds.

**Step-by-Step Instructions:**

1. **Go to Google Alerts**
   - Visit: https://www.google.com/alerts

2. **Create an Alert:**
   - **Search query:** Enter a query like:
     - `"need math tutor" OR "looking for math tutor"`
     - `"urgent math help" calculus OR precalculus`
     - `"math exam tomorrow" help`
   - **How often:** Select **"As-it-happens"** for real-time alerts
   - **Sources:** Select **"Automatic"** or choose specific sources
   - **Language:** Select your preferred language
   - **Region:** Select **"Any Region"** or your target region
   - **How many:** Select **"All results"**
   - **Deliver to:** Select **"RSS feed"**

3. **Create the Alert:**
   - Click **"Create Alert"**

4. **Get the RSS URL:**
   - After creating, click the RSS icon next to your alert
   - Copy the URL (it will look like: `https://www.google.com/alerts/feeds/...`)
   - You can create multiple alerts and add all RSS URLs to your configuration

5. **Important Notes:**
   - Create multiple alerts with different keywords for better coverage
   - Google Alerts can be noisy - the Gemini AI will filter out irrelevant results
   - Separate multiple RSS URLs with commas in the `.env` file

## Configuration

### 6. Create Your `.env` File

Create a file named `.env` in the same directory as `math_lead_sniper.py`:

```bash
# Reddit API Credentials
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=MathLeadSniper/1.0 by YourRedditUsername

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Discord Webhook URL
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here

# Google Alerts RSS URLs (optional, comma-separated)
GOOGLE_ALERTS_RSS_URLS=https://www.google.com/alerts/feeds/...,https://www.google.com/alerts/feeds/...
```

**Replace the placeholder values with your actual credentials:**

- `your_reddit_client_id_here` → Your Reddit client ID
- `your_reddit_client_secret_here` → Your Reddit client secret
- `YourRedditUsername` → Your Reddit username
- `your_gemini_api_key_here` → Your Google AI Studio API key
- `your_discord_webhook_url_here` → Your Discord webhook URL
- Add your Google Alerts RSS URLs (optional)

**Example:**

```bash
REDDIT_CLIENT_ID=abc123XYZ456
REDDIT_CLIENT_SECRET=xyz789ABC123def456GHI789
REDDIT_USER_AGENT=MathLeadSniper/1.0 by john_doe

GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuv
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/1234567890/abcdefghijklmnop

GOOGLE_ALERTS_RSS_URLS=https://www.google.com/alerts/feeds/12345/67890
```

### 7. Security Best Practices

- **Never commit your `.env` file to version control**
- Add `.env` to your `.gitignore` file
- Keep your API keys and secrets private
- Rotate your keys periodically
- Use environment variables in production

## Running the Math Lead Sniper

### 8. Start the Script

```bash
python math_lead_sniper.py
```

Or make it executable:

```bash
chmod +x math_lead_sniper.py
./math_lead_sniper.py
```

### 9. What to Expect

When running, you'll see:

```
2026-01-19 10:30:00 - __main__ - INFO - ============================================================
2026-01-19 10:30:00 - __main__ - INFO - 🎯 Math Lead Sniper Started!
2026-01-19 10:30:00 - __main__ - INFO - ============================================================
2026-01-19 10:30:00 - __main__ - INFO - Monitoring subreddits: HomeworkHelp, Calculus, LearnMath, MathHelp, PreCalculus
2026-01-19 10:30:00 - __main__ - INFO - Trigger keywords: urgent, exam, tutor, fail, due, stuck, help me, desperate, struggling, test tomorrow, quiz, homework due, need help, can someone, asap, deadline, final, midterm
2026-01-19 10:30:00 - __main__ - INFO - Cooldown period: 3600s
2026-01-19 10:30:00 - __main__ - INFO - ============================================================
2026-01-19 10:30:00 - __main__ - INFO - Reddit client initialized successfully
2026-01-19 10:30:00 - __main__ - INFO - Gemini AI initialized successfully
2026-01-19 10:30:00 - __main__ - INFO - Monitoring submissions from: HomeworkHelp, Calculus, LearnMath, MathHelp, PreCalculus
2026-01-19 10:30:00 - __main__ - INFO - Monitoring comments from: HomeworkHelp, Calculus, LearnMath, MathHelp, PreCalculus
```

### 10. Monitoring

- The script runs continuously and monitors Reddit in real-time
- When a potential lead is found, you'll see logs indicating analysis
- Qualified leads will trigger a Discord notification
- All activity is logged to `math_lead_sniper.log`

### 11. Stopping the Script

Press `Ctrl+C` to stop the script gracefully.

## Advanced Configuration

### Customizing Trigger Keywords

Edit the `TRIGGER_KEYWORDS` list in `math_lead_sniper.py`:

```python
TRIGGER_KEYWORDS = [
    'urgent', 'exam', 'tutor', 'fail', 'due', 'stuck',
    # Add your own keywords here
    'emergency', 'panic', 'lost', 'confused'
]
```

### Adjusting Cooldown Period

Change the `COOLDOWN_PERIOD` value (in seconds):

```python
COOLDOWN_PERIOD = 3600  # 1 hour (default)
COOLDOWN_PERIOD = 1800  # 30 minutes
COOLDOWN_PERIOD = 7200  # 2 hours
```

### Adding More Subreddits

Edit the `SUBREDDITS` list:

```python
SUBREDDITS = [
    'HomeworkHelp',
    'Calculus',
    'LearnMath',
    'MathHelp',
    'PreCalculus',
    # Add more subreddits
    'AskMath',
    'cheatatmathhomework',
    'statistics'
]
```

### Modifying the AI Prompt

Edit the `SYSTEM_INSTRUCTION` to change how Gemini evaluates leads:

```python
SYSTEM_INSTRUCTION = (
    "Your custom prompt here..."
)
```

## Troubleshooting

### Common Issues

**1. "Missing required environment variables"**
- Make sure your `.env` file exists and contains all required keys
- Check that there are no typos in the variable names

**2. "Failed to initialize Reddit client"**
- Verify your Reddit client ID and secret are correct
- Make sure you created a "script" type app, not a "web app"

**3. "Failed to initialize Gemini AI"**
- Verify your Gemini API key is correct
- Check that you have API access enabled in Google AI Studio

**4. "Discord webhook request failed"**
- Verify your webhook URL is correct
- Make sure the webhook hasn't been deleted
- Check that the channel still exists

**5. No leads are being detected**
- The script may be working correctly - leads are filtered strictly
- Check the log file for activity: `tail -f math_lead_sniper.log`
- Try lowering the AI filter threshold or adjusting trigger keywords

### Getting Help

- Check the log file: `math_lead_sniper.log`
- Verify your API keys and credentials
- Test each component individually
- Check rate limits on Reddit and Gemini APIs

## Running in Production

### Using systemd (Linux)

Create a systemd service file `/etc/systemd/system/math-lead-sniper.service`:

```ini
[Unit]
Description=Math Lead Sniper
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/money-printing-machine
ExecStart=/usr/bin/python3 /path/to/money-printing-machine/math_lead_sniper.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable math-lead-sniper
sudo systemctl start math-lead-sniper
sudo systemctl status math-lead-sniper
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY math_lead_sniper.py .
COPY .env .

CMD ["python", "math_lead_sniper.py"]
```

Build and run:

```bash
docker build -t math-lead-sniper .
docker run -d --name math-lead-sniper --restart unless-stopped math-lead-sniper
```

### Using screen or tmux

```bash
screen -S math-lead-sniper
python math_lead_sniper.py
# Press Ctrl+A, then D to detach

# Reattach later:
screen -r math-lead-sniper
```

## Cost Estimates

### Gemini API (Free Tier)
- **Free quota:** 15 requests per minute, 1,500 requests per day
- **Cost after free tier:** ~$0.00001 per request
- **Expected cost:** Free for typical usage

### Reddit API
- **Free:** Yes, but rate-limited to 60 requests per minute

### Discord Webhooks
- **Free:** Yes, unlimited

## Performance Tips

1. **Optimize trigger keywords** to reduce unnecessary Gemini API calls
2. **Adjust cooldown period** based on your volume needs
3. **Monitor logs** to fine-tune the AI prompt
4. **Use multiple Google Alerts** with specific queries

## Legal and Ethical Considerations

- Respect Reddit's Terms of Service and API usage policies
- Don't spam or harass users
- Only contact leads who explicitly ask for help
- Follow applicable data protection regulations
- Use the tool responsibly and ethically

## License

This tool is provided as-is for educational and business purposes.

## Support

For issues, questions, or feature requests, please refer to the project documentation.
