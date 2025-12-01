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
from mention_handler import MentionHandler

class TwitterAutomation:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.content_generator = ContentGenerator()
        self.twitter_poster = TwitterPoster()
        self.news_tracker = NewsTracker()
        self.mention_handler = MentionHandler()
        self.post_counter = 0  # Track post count for alternating
        self.ist = pytz.timezone('Asia/Kolkata')  # IST timezone
        
    def _get_post_type(self):
        """
        Randomly select post type (politics, stock_market, or trending)
        Uses date + minute as seed for consistent randomness per day, but different each run
        Returns: post_type: str where post_type is 'politics', 'stock_market', or 'trending'
        """
        # Get current time in IST
        current_time = datetime.now(self.ist)
        current_date = current_time.strftime('%Y-%m-%d')
        current_minute = current_time.minute
        
        # Use date + minute as seed for consistent randomness per day, but varied per run
        # This ensures we get roughly equal distribution (16 each) across 48 posts per day
        seed_string = f"{current_date}_{current_minute}_{random.random()}"
        seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16) % (10**8)
        random.seed(seed)
        
        # Equal probability for each type (33.33% each)
        # Target: ~16 politics, ~16 stock market, ~16 trending per day (48 total)
        rand = random.random()
        if rand < 0.333:
            return 'politics'
        elif rand < 0.666:
            return 'stock_market'
        else:
            return 'trending'
    
    def post_tweet(self, force_post=False):
        """
        Main function to fetch news, generate tweet, and post
        Always posts (skip logic removed for 48 tweets/day)
        force_post: Kept for compatibility but no longer needed (always posts)
        """
        current_time = datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S IST')
        trigger_type = "🔵 MANUAL TRIGGER" if force_post else "⏰ SCHEDULED RUN"
        print("\n" + "="*50)
        print(f"🚀 STARTING TWEET POSTING PROCESS")
        print(f"{trigger_type}")
        print(f"⏰ Time: {current_time}")
        print("="*50)
        
        # Always post - randomly select post type
        post_type_enum = self._get_post_type()
        
        # Map post type enum to display name
        post_type_map = {
            'politics': '🏛️  Politics',
            'stock_market': '📈 Stock Market',
            'trending': '🔥 Trending Topics'
        }
        post_type = post_type_map.get(post_type_enum, '📝 General')
        print(f"\n📌 Post type: {post_type} (random selection)")
        
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
            for trend in trending_topics[:15]:  # Check top 15 trends
                # Check if we've posted about this trend recently (by topic)
                trend_normalized = trend.replace('#', '').strip()
                # Create a title-like string for topic extraction
                trend_title = f"Trending: {trend_normalized}"
                if not self.news_tracker.is_already_posted('', trend_title, None, trend_title):
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
            
            # Add mentions for trending topics
            mentions = self.mention_handler.extract_mentions(
                tweet_text,
                is_stock_market=False,
                article_title=f"Trending: {trending_topic_to_post}",
                article_description=f"Current trending topic: {trending_topic_to_post}"
            )
            if mentions:
                print(f"🏷️  Extracted mentions: {', '.join(mentions)}")
                tweet_with_mentions = self.mention_handler.add_mentions_to_tweet(
                    tweet_text,
                    is_stock_market=False,
                    mentions=mentions
                )
                if tweet_with_mentions != tweet_text:
                    print(f"🏷️  Added mentions to tweet: {', '.join(mentions)}")
                    tweet_text = tweet_with_mentions
            
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
                article_description = article.get('description', '')
                
                # Check for duplicates before generating tweet (including topic check)
                if article_url and not self.news_tracker.is_already_posted(article_url, article_title, None, article_description):
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
        
        # STEP 6: Add relevant @mentions for maximum controversy and engagement
        print(f"✅ Generated tweet ({len(tweet_text)} chars)")
        print(f"📝 Preview: {tweet_text[:150]}...")
        
        # Add mentions based on content (with article context for better extraction)
        is_stock_market_type = (post_type_enum == 'stock_market')
        article_title = article_summary.get('title', '')
        article_description = article_summary.get('description', '')
        
        # Extract mentions with article context for better company/CEO detection
        mentions = self.mention_handler.extract_mentions(
            tweet_text, 
            is_stock_market=is_stock_market_type,
            article_title=article_title,
            article_description=article_description
        )
        
        if mentions:
            print(f"🏷️  Extracted mentions: {', '.join(mentions)}")
            tweet_with_mentions = self.mention_handler.add_mentions_to_tweet(
                tweet_text, 
                is_stock_market=is_stock_market_type,
                mentions=mentions
            )
            if tweet_with_mentions != tweet_text:
                print(f"🏷️  Added mentions to tweet: {', '.join(mentions)}")
                tweet_text = tweet_with_mentions
        
        # STEP 7: Final duplicate check on generated tweet content (including topic check)
        if self.news_tracker.is_already_posted(
            article_summary['url'], 
            article_summary['title'], 
            tweet_text,
            article_summary.get('description', '')
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
            # Mark as posted (including tweet text and topic for future duplicate detection)
            self.news_tracker.mark_as_posted(
                article_summary['url'],
                article_summary['title'],
                tweet_id,
                tweet_text,  # Store tweet text for duplicate checking
                article_summary.get('description', '')  # Store description for topic extraction
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
    else:
        # Default: run once
        print("Usage:")
        print("  python main.py --test           # Run once (test mode)")
        print("  python main.py --test --force   # Run once, always post (manual trigger)")
        print("\nRunning in test mode...\n")
        automation.run_once(force_post=force_post)

if __name__ == "__main__":
    main()

