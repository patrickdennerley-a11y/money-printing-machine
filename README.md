# Math Lead Sniper 🎯

> AI-Powered Math Tutoring Lead Monitor with Google Gemini Integration

## Overview

**Math Lead Sniper** is a high-precision lead monitoring system that automatically finds and qualifies math tutoring opportunities from Reddit and Google Alerts using AI. It filters out spam, ads, and low-quality posts, sending you only the most promising leads via Discord notifications.

### Key Features

- **Multi-Source Monitoring**: Tracks Reddit submissions, comments, and Google Alerts RSS feeds in real-time
- **AI-Powered Filtering**: Uses Google's Gemini 1.5 Flash to intelligently qualify leads
- **Smart Detection**: Keyword-based triggering with AI validation
- **Discord Integration**: Beautiful, formatted notifications sent directly to your Discord channel
- **Anti-Spam Protection**: Built-in cooldown mechanism prevents duplicate notifications
- **Robust Error Handling**: Automatic retry logic for network failures
- **Production Ready**: Multi-threaded design with comprehensive logging

## How It Works

```
┌─────────────────┐
│ Reddit & RSS    │
│ Monitoring      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Keyword Filter  │ ◄─── urgent, exam, tutor, stuck, etc.
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gemini AI       │ ◄─── "Is this a qualified lead?"
│ Analysis        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Discord         │
│ Notification    │ ◄─── Only high-quality leads
└─────────────────┘
```

### The AI Filter

When a post contains trigger keywords (like "urgent", "exam", "tutor", "fail", "due", "stuck"), the content is analyzed by Google's Gemini AI with this prompt:

> "You are a lead qualifier for a math tutor. Analyze the following text. Does the user explicitly express a desperate need for help, tutoring, or is struggling with an upcoming exam? If it is a spam bot, a promotional ad, a general discussion about math, or a rant with no intent to learn, return NO. If it is a student explicitly asking for help, return YES."

Only posts that receive a "YES" from Gemini trigger a Discord notification.

## Monitored Sources

### Reddit Subreddits
- r/HomeworkHelp
- r/Calculus
- r/LearnMath
- r/MathHelp
- r/PreCalculus

### Google Alerts (Optional)
- Monitor any custom search queries via RSS feeds
- Example: "need math tutor", "urgent calculus help", etc.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your API keys (see [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed steps):

```bash
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=MathLeadSniper/1.0 by YourUsername
GEMINI_API_KEY=your_gemini_key
DISCORD_WEBHOOK_URL=your_webhook_url
GOOGLE_ALERTS_RSS_URLS=your_rss_feeds  # Optional
```

### 3. Run the Sniper

```bash
python math_lead_sniper.py
```

You should see:

```
============================================================
🎯 Math Lead Sniper Started!
============================================================
Monitoring subreddits: HomeworkHelp, Calculus, LearnMath, MathHelp, PreCalculus
Trigger keywords: urgent, exam, tutor, fail, due, stuck, ...
Cooldown period: 3600s
============================================================
```

## Example Discord Notification

When a qualified lead is found, you'll receive a formatted Discord message like this:

```
🎯 High-Quality Lead Found!

Struggling with Calculus 2 - exam tomorrow!

📝 Snippet
I have a calculus 2 exam tomorrow and I'm completely stuck on integration by parts.
I've been trying for hours but can't figure it out. Does anyone know a tutor who
can help me tonight? I'm desperate!

🔗 Link
https://reddit.com/r/Calculus/comments/...

📍 Source: r/Calculus
⏰ Detected: 2026-01-19 14:30:45
```

## Architecture

### Components

1. **Reddit Stream Monitor**
   - Uses PRAW library to stream submissions and comments
   - Monitors multiple subreddits simultaneously
   - Handles rate limiting and network errors

2. **RSS Feed Monitor**
   - Uses feedparser to check Google Alerts RSS feeds
   - Polls every 5 minutes for new entries
   - Tracks seen entries to prevent duplicates

3. **Keyword Filter**
   - Pre-filters content based on trigger keywords
   - Reduces unnecessary API calls to Gemini
   - Customizable keyword list

4. **Gemini AI Analyzer**
   - Uses gemini-1.5-flash model (fast and cost-effective)
   - Analyzes content to determine if it's a qualified lead
   - Returns YES or NO based on system instruction

5. **Discord Notifier**
   - Sends rich embeds with formatted information
   - Includes title, snippet, link, source, and timestamp
   - Handles webhook failures gracefully

6. **Cooldown Manager**
   - Tracks processed content using MD5 hashes
   - Prevents duplicate notifications for the same post
   - Automatically cleans up old entries

### Multi-Threading

The system runs three concurrent threads:
- **Thread 1**: Reddit submissions monitoring
- **Thread 2**: Reddit comments monitoring
- **Thread 3**: RSS feeds monitoring (if configured)

Each thread has automatic retry logic with exponential backoff.

## Configuration

### Customizing Trigger Keywords

Edit `math_lead_sniper.py`:

```python
TRIGGER_KEYWORDS = [
    'urgent', 'exam', 'tutor', 'fail', 'due', 'stuck',
    # Add your own keywords
    'emergency', 'panic', 'lost'
]
```

### Adjusting Cooldown Period

```python
COOLDOWN_PERIOD = 3600  # Default: 1 hour
```

### Adding More Subreddits

```python
SUBREDDITS = [
    'HomeworkHelp',
    'Calculus',
    'LearnMath',
    'MathHelp',
    'PreCalculus',
    # Add more
    'AskMath',
    'statistics'
]
```

## API Costs

### Gemini 1.5 Flash (Google AI)
- **Free Tier**: 15 requests/minute, 1,500 requests/day
- **Paid Tier**: ~$0.00001 per request
- **Expected Cost**: Free for typical usage

### Reddit API
- **Free**: Yes, rate-limited to 60 requests/minute

### Discord Webhooks
- **Free**: Yes, unlimited

## Production Deployment

### Using systemd (Linux)

Create `/etc/systemd/system/math-lead-sniper.service`:

```ini
[Unit]
Description=Math Lead Sniper
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/money-printing-machine
ExecStart=/usr/bin/python3 math_lead_sniper.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable math-lead-sniper
sudo systemctl start math-lead-sniper
```

### Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY math_lead_sniper.py .
COPY .env .
CMD ["python", "math_lead_sniper.py"]
```

Build and run:

```bash
docker build -t math-lead-sniper .
docker run -d --restart unless-stopped math-lead-sniper
```

### Using screen/tmux

```bash
screen -S math-lead-sniper
python math_lead_sniper.py
# Ctrl+A, D to detach
```

## Logging

All activity is logged to `math_lead_sniper.log`:

```bash
# View logs in real-time
tail -f math_lead_sniper.log

# Search for qualified leads
grep "QUALIFIED LEAD" math_lead_sniper.log
```

## Troubleshooting

See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed troubleshooting steps.

### Quick Checks

1. **No leads detected?**
   - Check `math_lead_sniper.log` for activity
   - Verify trigger keywords are appropriate
   - The AI filter is strict - this is by design

2. **API errors?**
   - Verify all credentials in `.env`
   - Check API rate limits
   - Ensure internet connectivity

3. **Discord not receiving messages?**
   - Verify webhook URL is correct
   - Check webhook permissions
   - Test webhook manually: `curl -X POST -H "Content-Type: application/json" -d '{"content": "test"}' YOUR_WEBHOOK_URL`

## Files

```
money-printing-machine/
├── math_lead_sniper.py       # Main application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── SETUP_INSTRUCTIONS.md     # Detailed setup guide
└── math_lead_sniper.log      # Application logs (generated)
```

## Security

- Never commit `.env` to version control
- Keep API keys and secrets private
- Rotate credentials periodically
- Use environment variables in production
- Review webhook permissions

## Legal & Ethical Use

- Respect Reddit's Terms of Service and API policies
- Don't spam or harass users
- Only contact leads who explicitly request help
- Follow data protection regulations
- Use responsibly and ethically

## Technical Stack

- **Python 3.8+**
- **PRAW**: Reddit API wrapper
- **feedparser**: RSS feed parser
- **google-generativeai**: Google Gemini AI SDK
- **requests**: HTTP library for Discord webhooks
- **python-dotenv**: Environment variable management

## Performance

- **Memory Usage**: ~50-100MB
- **CPU Usage**: Minimal (<5%)
- **Network**: Depends on activity volume
- **Latency**: <2 seconds from post to notification

## Future Enhancements

Potential features for future versions:

- Web dashboard for monitoring
- Email notifications
- Slack integration
- Machine learning for better filtering
- Analytics and reporting
- Multi-language support
- Mobile app notifications

## Support

For detailed setup instructions, see [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md).

## License

This project is provided as-is for educational and business purposes.

---

**Built with ❤️ for math tutors who want to work smarter, not harder.**

*Stop wasting time scrolling through Reddit. Let AI find your best leads.*
