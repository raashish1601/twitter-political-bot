# Twitter Political Bot

An automated Twitter bot that posts controversial, engaging tweets about Indian politics, stock markets, and trending topics.

## Features

- 📰 **Politics**: Controversial tweets about Indian political news
- 📈 **Stock Market**: Provocative takes on Indian stock markets
- 🔥 **Trending Topics**: Controversial tweets about what's trending
- 🤖 AI-powered content generation with multiple API fallbacks (OpenAI, Groq, Hugging Face)
- 🐦 Automatic posting with images
- ⏰ Random posting times (48 posts per day)
- 📝 Smart duplicate prevention (URL, title, content, and topic-based)
- 🔥 Trending hashtags for maximum reach
- 🆓 Free API fallbacks when OpenAI is unavailable
- 🎯 Dynamic content generation (no hardcoded content)

## Post Types

- **Politics** (~16 posts/day): Highly controversial, offensive, strong language - BJP/NDA focused, brutally burns opposition
- **Stock Market** (~16 posts/day): Highly controversial, offensive, strong language - Market manipulation, FII/DII games exposed
- **Trending Topics** (~16 posts/day): Highly controversial, offensive, strong language - Brutal takes on trends

**Total: 48 posts per day** with random times throughout the day

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create `.env` file):
```
# Twitter API Credentials
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_token
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_secret

# News API
NEWS_API_KEY=your_key

# OpenAI API (primary)
OPENAI_API_KEY=your_key

# Optional: Free API fallbacks (recommended)
GROQ_API_KEY=your_groq_key
HUGGINGFACE_API_KEY=your_huggingface_key
```

3. Run the bot:
```bash
# Test mode (run once)
python main.py --test

# Manual trigger (always posts)
python main.py --test --force
```

## API Fallbacks

The bot uses a smart fallback system for content generation:

1. **OpenAI** (primary) - GPT-3.5-turbo for tweet generation
2. **Groq** (free fallback) - Fast, free API using Llama 3.1
3. **Hugging Face** (backup) - Free inference API
4. **Dynamic Template** (last resort) - Generates content from article text (no hardcoded content)

## Trending Topics

The bot fetches trending topics using multiple methods:

1. **Twitter Trends API** (requires higher access tier)
2. **Web Scraping** (may be blocked by Twitter)
3. **NewsAPI Fallback** (always works) - Generates trending topics from popular Indian news

## Deployment

Deployed for free using GitHub Actions. 

- **Schedule**: Runs every 30 minutes (48 times per day)
- **Posting**: Each run posts exactly 1 tweet (no skip logic)
- **Manual Triggers**: Always post (never skipped)
- **Random Times**: Posting times vary naturally throughout the day

### GitHub Secrets Required

Add these secrets to your GitHub repository:

- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_BEARER_TOKEN`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `NEWS_API_KEY`
- `OPENAI_API_KEY`
- `GROQ_API_KEY` (optional but recommended)
- `HUGGINGFACE_API_KEY` (optional)

## Content Generation

- **No Hardcoded Content**: All tweets are dynamically generated from news articles and trending topics
- **Controversial Style**: Highly offensive, provocative language designed to create debate
- **Smart Hashtags**: Automatically extracts and includes relevant hashtags from content
- **Duplicate Prevention**: Multi-layer system prevents posting similar content
