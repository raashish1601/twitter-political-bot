# Twitter Political Bot

An automated Twitter bot that posts controversial, funky tweets about Indian politics, stock markets, and trending topics. Designed to create maximum engagement through provocative content.

## 🚀 Features

- 📰 **Politics Posts** (~6 per day) - Controversial takes on Indian political news
- 📈 **Stock Market Posts** (~6 per day) - Provocative market analysis and exposes
- 🔥 **Trending Topics Posts** (~3-4 per day) - Controversial takes on what's trending
- 🖼️ **Image Support** - Automatically includes images from news articles
- 🏷️ **Trending Hashtags** - Integrates top trending hashtags for maximum reach
- ⏰ **Random Posting Times** - Different times each day (doesn't look automated)
- 🚫 **No Duplicates** - Triple-layer duplicate detection (URL, title, content)
- 🔵 **Manual Triggers** - Always post when manually triggered (never skip)
- 📊 **Detailed Logging** - See all runs (posted and skipped) with reasons

## 📊 Daily Posting Schedule

- **Total Posts**: ~15-16 per day
- **Politics**: ~6 posts
- **Stock Market**: ~6 posts  
- **Trending Topics**: ~3-4 posts
- **Schedule**: Runs every 2 hours, bot decides randomly when to post
- **Posting Windows**: 7 AM - 10 PM IST

## 🎯 Content Style

All tweets are designed to be:
- **Highly Controversial** - Creates debate and engagement
- **Funky & Witty** - Savage humor and clever wordplay
- **Viral-Worthy** - Designed to get maximum shares and comments
- **Trending-Focused** - Includes top trending hashtags for reach

## 🛠️ Setup

### Prerequisites

- Python 3.11+
- Twitter API credentials (from [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard))
- NewsAPI key (from [NewsAPI.org](https://newsapi.org/))
- OpenAI API key (from [OpenAI Platform](https://platform.openai.com/api-keys))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/raashish1601/twitter-political-bot.git
cd twitter-political-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Run the setup script
bash setup_env.sh

# Or manually create .env file with:
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_token
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_secret
NEWS_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## 🚀 Usage

### Local Testing

```bash
# Test mode (run once)
python main.py --test

# Test mode with force post (always posts)
python main.py --test --force

# Scheduled mode (runs continuously)
python main.py --scheduled
```

### Deployment (GitHub Actions - FREE)

The bot is configured to run automatically on GitHub Actions:

1. **Add Secrets** to your GitHub repository:
   - Go to: Settings → Secrets and variables → Actions
   - Add all 7 secrets from your `.env` file

2. **Automatic Runs**: 
   - Runs every 2 hours automatically
   - Bot decides randomly when to post (to avoid looking automated)

3. **Manual Triggers**:
   - Go to Actions tab → Twitter Bot Scheduler
   - Click "Run workflow" → Always posts (never skips)

## 📁 Project Structure

```
twitter-political-bot/
├── main.py                 # Main bot logic and orchestration
├── news_fetcher.py         # Fetches news from NewsAPI
├── content_generator.py   # Generates controversial tweets (OpenAI + fallback)
├── twitter_poster.py      # Posts tweets with image support
├── news_tracker.py         # Tracks posted content (duplicate prevention)
├── scheduler.py            # Handles posting schedule
├── requirements.txt        # Python dependencies
├── .github/workflows/      # GitHub Actions workflow
└── README.md              # This file
```

## 🔒 Duplicate Prevention

The bot uses triple-layer duplicate detection:

1. **URL Matching** - Exact URL comparison
2. **Title Similarity** - 85% similarity threshold
3. **Content Similarity** - 80% similarity threshold for tweet text

Tracks posted content for 30 days to avoid duplicates.

## 📈 Free Tier Limits

- **Twitter API**: 1,500 tweets/month (free tier) ✅
- **GitHub Actions**: Unlimited (public repos) ✅
- **NewsAPI**: 100 requests/day ✅
- **OpenAI API**: Pay-as-you-go (~$0.18/month for 90 tweets)

Current usage: ~450 tweets/month - **Well within free tier limits!**

## 🎨 Content Types

### Politics Posts
- Pro-BJP/NDA bias
- Burns opposition with savage humor
- Exposes corruption and questions policies
- Creates debate on sensitive issues

### Stock Market Posts
- Exposes market manipulation hints
- Questions broker recommendations
- Creates FOMO or fear
- Challenges mainstream narratives

### Trending Topics Posts
- Controversial takes on what's trending
- Exposes hidden truths behind trends
- Questions why topics are trending
- Creates massive debate and engagement

## 🔧 Configuration

### Posting Times
- Random times throughout the day (7 AM - 10 PM IST)
- Different times each day (date-based randomness)
- Manual triggers always post immediately

### Content Generation
- Uses OpenAI GPT-3.5-turbo for controversial content
- Falls back to rule-based generator if OpenAI fails
- Temperature: 1.0 (maximum creativity and controversy)

## 📝 Logging

All runs are logged with detailed information:
- ✅ Successful posts (with tweet ID and URL)
- ⏸️ Skipped runs (with reason)
- ❌ Failed posts (with error details)
- 🔵 Manual triggers (always post)

View logs in: GitHub Actions → Twitter Bot Scheduler → Run details

## 🤝 Contributing

Feel free to fork, modify, and use this bot for your own purposes!

## ⚠️ Disclaimer

This bot generates controversial content designed to create engagement. Use responsibly and ensure compliance with Twitter's Terms of Service.

## 📄 License

This project is open source and available for personal use.

---

**Made with ❤️ for maximum Twitter engagement**
