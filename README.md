# Twitter Political Bot

An automated Twitter bot that fetches the latest Indian political news and posts engaging tweets 2-3 times daily.

## Features

- 📰 Fetches latest Indian political news from NewsAPI
- 🤖 Generates engaging tweets using OpenAI
- 🐦 Posts to Twitter automatically
- ⏰ Scheduled posting at optimal times (8:30 AM, 1:30 PM, 8:00 PM IST)
- 🔥 Integrates trending topics for maximum reach
- 📝 Tracks posted articles to avoid duplicates

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create `.env` file):
```
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_token
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_secret
NEWS_API_KEY=your_key
OPENAI_API_KEY=your_key
```

3. Run the bot:
```bash
# Test mode (run once)
python main.py --test

# Scheduled mode (runs continuously)
python main.py --scheduled
```

## Deployment

This bot can be deployed for free using GitHub Actions. See the `.github/workflows/` directory for the workflow configuration.
