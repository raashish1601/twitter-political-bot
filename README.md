# Twitter Political Bot

An automated Twitter bot that posts controversial, engaging tweets about Indian politics, stock markets, and trending topics.

## Features

- 📰 **Politics**: Controversial tweets about Indian political news
- 📈 **Stock Market**: Provocative takes on Indian stock markets
- 🔥 **Trending Topics**: Controversial tweets about what's trending
- 🤖 AI-powered content generation with OpenAI
- 🐦 Automatic posting with images
- ⏰ Random posting times (18 posts per day)
- 📝 Smart duplicate prevention
- 🔥 Trending hashtags for maximum reach

## Post Types

- **Politics** (6 posts/day): Highly controversial, offensive, strong language - BJP/NDA focused, brutally burns opposition
- **Stock Market** (6 posts/day): Highly controversial, offensive, strong language - Market manipulation, FII/DII games exposed
- **Trending Topics** (6 posts/day): Highly controversial, offensive, strong language - Brutal takes on trends

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

# Manual trigger (always posts)
python main.py --test --force
```

## Deployment

Deployed for free using GitHub Actions. Runs every 2 hours automatically with random posting logic. Manual triggers always post.
