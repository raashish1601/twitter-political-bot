#!/bin/bash

# Setup script to create .env file
# Run this script to set up your environment variables

cat > .env << 'EOF'
# Twitter API Credentials
# Get these from https://developer.twitter.com/en/portal/dashboard
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here

# News API
# Get your API key from https://newsapi.org/
NEWS_API_KEY=your_news_api_key_here

# OpenAI API
# Get your API key from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here
EOF

echo "✅ .env file created successfully!"
