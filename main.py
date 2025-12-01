"""
Main Twitter Automation Script
Fetches latest Indian political and stock market news and posts controversial funky tweets with random timing
"""
import sys
import os
import random
import hashlib
from datetime import datetime
import pytz
from news_fetcher import NewsFetcher
from content_generator import ContentGenerator
from twitter_poster import TwitterPoster
from news_tracker import NewsTracker
from scheduler import TweetScheduler

class TwitterAutomation:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.content_generator = ContentGenerator()
        self.twitter_poster = TwitterPoster()
        self.news_tracker = NewsTracker()
        self.post_counter = 0  # Track post count for alternating
        self.ist = pytz.timezone('Asia/Kolkata')  # IST timezone
        
    def _should_post_now(self, force_post=False):
        """
        Randomly decide if we should post now (to avoid looking automated)
        Uses date-based seed for consistent randomness per day, but different each day
        If force_post is True (manual trigger), always returns True
        Returns: (should_post: bool, post_type: str) where post_type is 'politics', 'stock_market', or 'trending'
        """
        # Get current time in IST
        current_time = datetime.now(self.ist)
        current_hour = current_time.hour
        
        # Manual triggers should never skip
        if force_post:
            # Still determine type randomly but always post
            rand = random.random()
            if rand < 0.33:
                return True, 'politics'
            elif rand < 0.66:
                return True, 'stock_market'
            else:
                return True, 'trending'
        
        current_date = current_time.strftime('%Y-%m-%d')
        
        # Use date + hour as seed for consistent randomness per day
        seed_string = f"{current_date}_{current_hour}"
        seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16) % (10**8)
        random.seed(seed)
        
        # Define time windows for posting (spread throughout the day)
        morning_window = (7, 11)    # 7 AM - 11 AM
        afternoon_window = (12, 16)  # 12 PM - 4 PM
        evening_window = (17, 22)    # 5 PM - 10 PM
        
        # Check if current hour is in any window
        in_morning = morning_window[0] <= current_hour < morning_window[1]
        in_afternoon = afternoon_window[0] <= current_hour < afternoon_window[1]
        in_evening = evening_window[0] <= current_hour < evening_window[1]
        
        if not (in_morning or in_afternoon or in_evening):
            return False, False  # Outside posting windows
        
        # Random probability based on window (higher during peak hours)
        if in_morning:
            post_probability = random.uniform(0.3, 0.5)  # 30-50% chance
        elif in_afternoon:
            post_probability = random.uniform(0.4, 0.6)  # 40-60% chance
        else:  # evening
            post_probability = random.uniform(0.35, 0.55)  # 35-55% chance
        
        # Decide if we should post
        should_post = random.random() < post_probability
        
        if not should_post:
            return False, False
        
        # Determine post type based on hour and random factor
        # Distribution: ~6 politics, ~6 stock market, ~3-4 trending per day
        # Stock market: prefer 9-11 AM, 2-4 PM, 5-7 PM
        # Politics: prefer 7-9 AM, 12-2 PM, 6-10 PM
        # Trending: spread throughout the day (3-4 posts)
        
        stock_market_preferred = (
            (9 <= current_hour < 11) or  # Morning trading
            (14 <= current_hour < 16) or  # Afternoon trading
            (17 <= current_hour < 19)     # Market close/evening
        )
        
        politics_preferred = (
            (7 <= current_hour < 9) or   # Early morning
            (12 <= current_hour < 14) or  # Lunch/afternoon
            (18 <= current_hour < 22)     # Evening/night
        )
        
        # Randomly decide type with bias toward preferred times
        rand = random.random()
        
        if stock_market_preferred:
            # Higher chance for stock market during trading hours
            if rand < 0.50:
                return True, 'stock_market'
            elif rand < 0.75:
                return True, 'politics'
            else:
                return True, 'trending'
        elif politics_preferred:
            # Higher chance for politics during preferred hours
            if rand < 0.50:
                return True, 'politics'
            elif rand < 0.75:
                return True, 'stock_market'
            else:
                return True, 'trending'
        else:
            # Other hours - more balanced, trending gets more chance
            if rand < 0.40:
                return True, 'politics'
            elif rand < 0.70:
                return True, 'stock_market'
            else:
                return True, 'trending'
    
    def post_tweet(self, force_post=False):
        """
        Main function to fetch news, generate tweet, and post
        Alternates between political and stock market news
        force_post: If True, always posts (for manual triggers)
        """
        current_time = datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S IST')
        trigger_type = "🔵 MANUAL TRIGGER" if force_post else "⏰ SCHEDULED RUN"
        print("\n" + "="*50)
        print(f"🚀 STARTING TWEET POSTING PROCESS")
        print(f"{trigger_type}")
        print(f"⏰ Time: {current_time}")
        print("="*50)
        
        # Randomly decide if we should post now (to avoid looking automated)
        # Manual triggers always post
        should_post, post_type_enum = self._should_post_now(force_post=force_post)
        # current_time already set above, reuse it
        
        if not should_post:
            print("\n" + "="*50)
            print(f"⏸️  SKIP DECISION")
            print(f"⏰ Time: {current_time}")
            print(f"📊 Decision: Not posting at this time")
            print(f"💡 Reason: Randomized schedule (to avoid looking automated)")
            print(f"✅ Status: Skipped successfully")
            print(f"ℹ️  Note: Manual triggers always post (use 'Run workflow' button)")
            print("="*50)
            return
        
        # Map post type enum to display name
        post_type_map = {
            'politics': '🏛️  Politics',
            'stock_market': '📈 Stock Market',
            'trending': '🔥 Trending Topics'
        }
        post_type = post_type_map.get(post_type_enum, '📝 General')
        print(f"\n📌 Post type: {post_type} (random time)")
        
        # STEP 1: Fetch trending topics FIRST (always needed)
        print("\n🔥 Fetching Twitter trends...")
        trending_topics = self.twitter_poster.get_trending_topics()
        if trending_topics:
            print(f"✅ Found {len(trending_topics)} trending topics")
            print(f"   🔥 Top trends: {', '.join(trending_topics[:5])}")
        else:
            print("⚠️  Could not fetch trends, continuing without them...")
            trending_topics = []
        
        # STEP 2: Handle different post types
        if post_type_enum == 'trending':
            # For trending posts, create tweet directly from trending topics
            if not trending_topics:
                print("\n" + "="*50)
                print(f"⏸️  SKIP DECISION")
                print(f"⏰ Time: {current_time}")
                print(f"📌 Type: {post_type}")
                print(f"❌ Reason: No trending topics found")
                print(f"✅ Status: Skipped (no trending content available)")
                print("="*50)
                return
            
            # Select a trending topic that hasn't been posted about
            trending_topic_to_post = None
            for trend in trending_topics[:10]:  # Check top 10 trends
                # Check if we've posted about this trend recently
                trend_normalized = trend.replace('#', '').lower().strip()
                if not self.news_tracker.is_already_posted('', trend_normalized):
                    trending_topic_to_post = trend
                    break
            
            if not trending_topic_to_post:
                print("\n" + "="*50)
                print(f"⏸️  SKIP DECISION")
                print(f"⏰ Time: {current_time}")
                print(f"📌 Type: {post_type}")
                print(f"⚠️  Reason: All trending topics already posted")
                print(f"✅ Status: Skipped (avoiding duplicates)")
                print("="*50)
                return
            
            print(f"\n🔥 Selected trending topic: {trending_topic_to_post}")
            
            # Generate controversial tweet about trending topic
            print(f"\n🤖 Generating CONTROVERSIAL, funky tweet about trending topic...")
            tweet_text = self.content_generator.generate_trending_tweet(
                trending_topic_to_post,
                trending_topics
            )
            
            # Create fake article summary for tracking
            article_summary = {
                'title': f"Trending: {trending_topic_to_post}",
                'description': f"Current trending topic on Twitter: {trending_topic_to_post}",
                'url': f"https://twitter.com/search?q={trending_topic_to_post.replace('#', '%23')}",
                'source': 'Twitter Trends',
                'published_at': datetime.now(self.ist).isoformat(),
                'image_url': ''  # Trending topics don't have images
            }
            
        else:
            # For politics and stock market, fetch news articles
            if post_type_enum == 'stock_market':
                print("\n📈 Fetching latest stock market news...")
                articles = self.news_fetcher.fetch_stock_market_news(max_results=15)
            else:  # politics
                print("\n📰 Fetching latest political news...")
                articles = self.news_fetcher.fetch_latest_news(max_results=15)
            
            if not articles:
                print("\n" + "="*50)
                print(f"⏸️  SKIP DECISION")
                print(f"⏰ Time: {current_time}")
                print(f"📌 Type: {post_type}")
                print(f"❌ Reason: No articles found")
                print(f"✅ Status: Skipped (no content available)")
                print("="*50)
                return
            
            print(f"✅ Found {len(articles)} articles")
            
            # STEP 3: Prioritize articles that match trending topics
            if trending_topics:
                articles = self.news_fetcher.prioritize_by_trends(articles, trending_topics)
                print(f"📊 Re-prioritized articles based on trending topics")
            
            # STEP 4: Find an article that hasn't been posted
            article_to_post = None
            for article in articles:
                article_url = article.get('url', '')
                article_title = article.get('title', '')
                
                # Check for duplicates before generating tweet
                if article_url and not self.news_tracker.is_already_posted(article_url, article_title):
                    article_to_post = article
                    break
            
            if not article_to_post:
                print("\n" + "="*50)
                print(f"⏸️  SKIP DECISION")
                print(f"⏰ Time: {current_time}")
                print(f"📌 Type: {post_type}")
                print(f"⚠️  Reason: All recent articles already posted")
                print(f"✅ Status: Skipped (avoiding duplicates)")
                print("="*50)
                return
            
            # Get article summary
            article_summary = self.news_fetcher.get_article_summary(article_to_post)
            print(f"\n📄 Selected article: {article_summary['title'][:80]}...")
            
            # STEP 5: Generate controversial funky tweet with TRENDING PRIORITY
            print(f"\n🤖 Generating CONTROVERSIAL, funky tweet with TRENDING hashtags...")
            tweet_text = self.content_generator.generate_funky_tweet(
                article_summary, 
                trending_topics, 
                is_stock_market=(post_type_enum == 'stock_market')
            )
        
        # STEP 6: Final duplicate check on generated tweet content (for all types)
        print(f"✅ Generated tweet ({len(tweet_text)} chars)")
        print(f"📝 Preview: {tweet_text[:150]}...")
        
        # STEP 7: Final duplicate check on generated tweet content
        if self.news_tracker.is_already_posted(
            article_summary['url'], 
            article_summary['title'], 
            tweet_text
        ):
            print("\n" + "="*50)
            print(f"⏸️  SKIP DECISION")
            print(f"⏰ Time: {current_time}")
            print(f"📌 Type: {post_type}")
            print(f"🚫 Reason: Generated tweet too similar to previous post")
            print(f"✅ Status: Skipped (avoiding duplicate content)")
            print("="*50)
            return
        
        # Post to Twitter with image if available
        print("\n🐦 Posting to Twitter...")
        image_url = article_summary.get('image_url', '')
        if image_url:
            print(f"🖼️  Article has image, will include in tweet")
        success, tweet_id = self.twitter_poster.post_tweet(tweet_text, image_url=image_url)
        
        if success:
            # Mark as posted (including tweet text for future duplicate detection)
            self.news_tracker.mark_as_posted(
                article_summary['url'],
                article_summary['title'],
                tweet_id,
                tweet_text  # Store tweet text for duplicate checking
            )
            print("\n" + "="*50)
            print(f"✅ TWEET POSTED SUCCESSFULLY!")
            print(f"📝 Tweet ID: {tweet_id}")
            print(f"📌 Type: {post_type}")
            print(f"⏰ Posted at: {current_time}")
            print(f"🔗 URL: https://twitter.com/i/web/status/{tweet_id}")
            print("="*50)
            self.post_counter += 1
        else:
            print("\n" + "="*50)
            print(f"❌ FAILED TO POST TWEET")
            print(f"⏰ Time: {current_time}")
            print(f"📌 Type: {post_type}")
            print(f"⚠️  Status: Posting failed")
            print("="*50)
    
    def test_connection(self):
        """
        Test all connections and credentials
        """
        print("🔍 Testing connections...\n")
        
        # Test Twitter
        print("1. Testing Twitter API...")
        if self.twitter_poster.verify_credentials():
            print("   ✅ Twitter API: Connected\n")
        else:
            print("   ❌ Twitter API: Failed\n")
            return False
        
        # Test News API
        print("2. Testing News API...")
        articles = self.news_fetcher.fetch_latest_news(max_results=1)
        if articles:
            print(f"   ✅ News API: Connected (found {len(articles)} articles)\n")
        else:
            print("   ❌ News API: Failed\n")
            return False
        
        # Test OpenAI
        print("3. Testing OpenAI API...")
        try:
            test_article = {'title': 'Test', 'description': 'Test description', 'source': 'Test'}
            tweet = self.content_generator.generate_funky_tweet(test_article, None)
            if tweet:
                print(f"   ✅ OpenAI API: Connected\n")
            else:
                print("   ❌ OpenAI API: Failed\n")
                return False
        except Exception as e:
            print(f"   ⚠️  OpenAI API: {str(e)[:50]}... (will use fallback)\n")
            # Don't fail if OpenAI is down, we have fallback
        
        print("✅ All connections successful!")
        return True
    
    def run_scheduled(self):
        """
        Run with scheduler (for continuous operation)
        """
        print("\n" + "="*50)
        print("🚀 Twitter Automation Bot Starting...")
        print("="*50)
        
        # Test connections first
        if not self.test_connection():
            print("\n❌ Connection test failed. Please check your credentials.")
            return
        
        # Cleanup old entries (keep 30 days for better duplicate prevention)
        self.news_tracker.cleanup_old_entries(days=30)
        
        # Setup scheduler
        scheduler = TweetScheduler(self.post_tweet)
        scheduler.setup_schedule()
        
        # Post immediately once (optional - remove if you don't want this)
        # print("\n📤 Posting first tweet now...")
        # self.post_tweet()
        
        # Run scheduler
        try:
            scheduler.run()
        except KeyboardInterrupt:
            print("\n\n⏹️  Scheduler stopped by user.")
            sys.exit(0)
    
    def run_once(self, force_post=False):
        """
        Run once (for testing or manual execution)
        force_post: If True, always posts (for manual triggers)
        """
        print("\n" + "="*50)
        if force_post:
            print("🔵 Running once (MANUAL TRIGGER - will always post)...")
        else:
            print("🧪 Running once (test mode)...")
        print("="*50)
        
        if not self.test_connection():
            print("\n❌ Connection test failed. Please check your credentials.")
            return
        
        self.post_tweet(force_post=force_post)

def main():
    automation = TwitterAutomation()
    
    # Check command line arguments
    force_post = '--force' in sys.argv
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test mode - run once (with optional force flag)
        automation.run_once(force_post=force_post)
    elif len(sys.argv) > 1 and sys.argv[1] == '--scheduled':
        # Scheduled mode - run continuously
        automation.run_scheduled()
    else:
        # Default: run once
        print("Usage:")
        print("  python main.py --test           # Run once (test mode)")
        print("  python main.py --test --force   # Run once, always post (manual trigger)")
        print("  python main.py --scheduled      # Run with scheduler (production)")
        print("\nRunning in test mode...\n")
        automation.run_once(force_post=force_post)

if __name__ == "__main__":
    main()

