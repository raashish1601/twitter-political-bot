"""
Twitter Poster Module - Posts tweets using Twitter API v2
"""
import tweepy
import os
import requests
import tempfile
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
    
        # Initialize API v1.1 for media uploads (required for images)
        auth = tweepy.OAuth1UserHandler(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret
        )
        self.api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
    
    def _download_image(self, image_url):
        """
        Download image from URL and return temporary file path
        """
        try:
            if not image_url or image_url == 'null' or not image_url.startswith('http'):
                return None
            
            print(f"📥 Downloading image from: {image_url[:50]}...")
            response = requests.get(image_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print("⚠️  URL is not an image, skipping...")
                return None
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            temp_file.write(response.content)
            temp_file.close()
            
            print(f"✅ Image downloaded: {len(response.content)} bytes")
            return temp_file.name
            
        except Exception as e:
            print(f"⚠️  Could not download image: {e}")
            return None
    
    def _upload_media(self, image_path):
        """
        Upload image to Twitter and return media_id
        """
        try:
            if not image_path or not os.path.exists(image_path):
                return None
            
            print(f"📤 Uploading image to Twitter...")
            media = self.api_v1.media_upload(image_path)
            print(f"✅ Image uploaded! Media ID: {media.media_id}")
            return media.media_id
            
        except Exception as e:
            print(f"⚠️  Could not upload image: {e}")
            return None
    
    def post_tweet(self, tweet_text, image_url=None):
        """
        Post a tweet to Twitter with optional image
        """
        media_id = None
        temp_image_path = None
        
        try:
            # Download and upload image if provided
            if image_url:
                temp_image_path = self._download_image(image_url)
                if temp_image_path:
                    media_id = self._upload_media(temp_image_path)
            
            # Ensure tweet is within character limit
            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."
            
            # Post the tweet with or without media
            if media_id:
                response = self.client.create_tweet(text=tweet_text, media_ids=[media_id])
                print("📸 Tweet posted with image!")
            else:
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
        finally:
            # Clean up temporary image file
            if temp_image_path and os.path.exists(temp_image_path):
                try:
                    os.unlink(temp_image_path)
                except:
                    pass
    
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
        Falls back to NewsAPI if Twitter trends API is not available
        """
        try:
            # Use existing API v1.1 instance for trends (v2 doesn't have trends endpoint)
            trends = self.api_v1.get_place_trends(woeid)
            
            if trends and len(trends) > 0:
                trending_list = [trend['name'] for trend in trends[0]['trends'][:10]]
                return trending_list
            return []
        except Exception as e:
            error_msg = str(e)
            if '403' in error_msg or 'Forbidden' in error_msg:
                print(f"⚠️  Twitter trends API not available (requires higher access level)")
                print(f"🔄 Falling back to NewsAPI for trending topics...")
                return self._get_trending_from_newsapi()
            else:
                print(f"⚠️  Could not fetch trends: {e}")
                return self._get_trending_from_newsapi()
    
    def _get_trending_from_newsapi(self):
        """
        Fallback: Get trending topics from NewsAPI by fetching popular news
        """
        try:
            import os
            from datetime import datetime, timedelta
            news_api_key = os.getenv('NEWS_API_KEY')
            
            if not news_api_key:
                print("⚠️  NEWS_API_KEY not found, cannot fetch trending topics")
                return []
            
            # Fetch popular news from India (sorted by popularity/relevancy)
            base_url = 'https://newsapi.org/v2/everything'
            from_date = (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%dT%H:%M:%S')
            
            params = {
                'q': 'India OR Indian',
                'language': 'en',
                'sortBy': 'popularity',  # Sort by popularity to get trending topics
                'pageSize': 20,
                'from': from_date,
                'apiKey': news_api_key
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                
                # Extract trending topics from article titles
                trending_topics = []
                seen_topics = set()
                
                for article in articles[:15]:
                    title = article.get('title', '')
                    if title:
                        # Extract key terms from title (remove common words)
                        words = title.split()
                        # Get capitalized words or important terms (length > 4)
                        key_terms = []
                        for word in words:
                            word_clean = word.strip('.,!?;:()[]{}"\'').strip()
                            # Include if it's capitalized (likely a name/topic) or is a significant word
                            if (word_clean and len(word_clean) > 4 and 
                                (word_clean[0].isupper() or word_clean.lower() not in 
                                 ['india', 'indian', 'news', 'latest', 'breaking', 'update', 'report', 'says', 'will', 'this', 'that', 'with', 'from', 'about'])):
                                key_terms.append(word_clean)
                        
                        # Create topic from key terms
                        if key_terms:
                            topic = ' '.join(key_terms[:3])  # Take first 3 key terms
                            topic_normalized = topic.lower()
                            if topic_normalized not in seen_topics and len(topic) > 5:
                                trending_topics.append(topic)
                                seen_topics.add(topic_normalized)
                
                # Also add hashtag versions
                hashtag_topics = [f"#{topic.replace(' ', '')}" if not topic.startswith('#') else topic 
                                 for topic in trending_topics[:10]]
                
                print(f"✅ Generated {len(hashtag_topics)} trending topics from NewsAPI")
                return hashtag_topics[:10]
            
            return []
        except Exception as e:
            print(f"⚠️  Could not fetch trending topics from NewsAPI: {e}")
            return []

