"""
Twitter Poster Module - Posts tweets using Twitter API v2
"""
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterPoster:
    def __init__(self):
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # Initialize Twitter API v2 client with OAuth 1.0a for write operations
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            wait_on_rate_limit=True
        )
    
    def post_tweet(self, tweet_text):
        """
        Post a tweet to Twitter
        """
        try:
            # Ensure tweet is within character limit
            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."
            
            # Post the tweet
            response = self.client.create_tweet(text=tweet_text)
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✅ Tweet posted successfully! Tweet ID: {tweet_id}")
                print(f"📝 Tweet: {tweet_text[:100]}...")
                return True, tweet_id
            else:
                print("❌ Failed to post tweet: No response data")
                return False, None
                
        except tweepy.TooManyRequests:
            print("❌ Rate limit exceeded. Please wait before posting again.")
            return False, None
        except tweepy.Unauthorized:
            print("❌ Unauthorized: Check your Twitter API credentials")
            return False, None
        except Exception as e:
            print(f"❌ Error posting tweet: {e}")
            return False, None
    
    def verify_credentials(self):
        """
        Verify Twitter API credentials
        """
        try:
            me = self.client.get_me()
            if me.data:
                print(f"✅ Twitter API connected! Logged in as: @{me.data.username}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error verifying credentials: {e}")
            return False
    
    def get_trending_topics(self, woeid=23424848):
        """
        Get trending topics for India (woeid 23424848)
        Returns list of trending topic names
        """
        try:
            # Use API v1.1 for trends (v2 doesn't have trends endpoint)
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            api_v1 = tweepy.API(auth)
            
            # Get trends for India
            trends = api_v1.get_place_trends(woeid)
            
            if trends and len(trends) > 0:
                trending_list = [trend['name'] for trend in trends[0]['trends'][:10]]
                return trending_list
            return []
        except Exception as e:
            print(f"⚠️  Could not fetch trends: {e}")
            return []

