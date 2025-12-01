"""
Main Twitter Automation Script
Fetches latest Indian political news and posts funky tweets 2-3 times daily
"""
import sys
import os
from datetime import datetime
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
        
    def post_tweet(self):
        """
        Main function to fetch news, generate tweet, and post
        PRIORITY: Trending topics for maximum reach
        """
        print("\n" + "="*50)
        print(f"🔄 Starting tweet posting process...")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        # STEP 1: Fetch trending topics FIRST (priority for maximum reach)
        print("\n🔥 Fetching Twitter trends (PRIORITY)...")
        trending_topics = self.twitter_poster.get_trending_topics()
        if trending_topics:
            print(f"✅ Found {len(trending_topics)} trending topics")
            print(f"   🔥 Top trends: {', '.join(trending_topics[:5])}")
        else:
            print("⚠️  Could not fetch trends, continuing without them...")
            trending_topics = []
        
        # STEP 2: Fetch latest news
        print("\n📰 Fetching latest news...")
        articles = self.news_fetcher.fetch_latest_news(max_results=15)
        
        if not articles:
            print("❌ No news articles found. Skipping this post.")
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
            if article_url and not self.news_tracker.is_already_posted(article_url):
                article_to_post = article
                break
        
        if not article_to_post:
            print("⚠️  All recent articles have already been posted. Skipping.")
            return
        
        # Get article summary
        article_summary = self.news_fetcher.get_article_summary(article_to_post)
        print(f"\n📄 Selected article: {article_summary['title'][:80]}...")
        
        # STEP 5: Generate funky tweet with TRENDING PRIORITY
        print("\n🤖 Generating funky, ass-burning tweet with TRENDING hashtags...")
        tweet_text = self.content_generator.generate_funky_tweet(article_summary, trending_topics)
        print(f"✅ Generated tweet ({len(tweet_text)} chars)")
        print(f"📝 Preview: {tweet_text[:150]}...")
        
        # Post to Twitter with image if available
        print("\n🐦 Posting to Twitter...")
        image_url = article_summary.get('image_url', '')
        if image_url:
            print(f"🖼️  Article has image, will include in tweet")
        success, tweet_id = self.twitter_poster.post_tweet(tweet_text, image_url=image_url)
        
        if success:
            # Mark as posted
            self.news_tracker.mark_as_posted(
                article_summary['url'],
                article_summary['title'],
                tweet_id
            )
            print("\n✅ Tweet posted successfully!")
        else:
            print("\n❌ Failed to post tweet.")
    
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
        
        # Cleanup old entries
        self.news_tracker.cleanup_old_entries(days=7)
        
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
    
    def run_once(self):
        """
        Run once (for testing or manual execution)
        """
        print("\n" + "="*50)
        print("🧪 Running once (test mode)...")
        print("="*50)
        
        if not self.test_connection():
            print("\n❌ Connection test failed. Please check your credentials.")
            return
        
        self.post_tweet()

def main():
    automation = TwitterAutomation()
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test mode - run once
        automation.run_once()
    elif len(sys.argv) > 1 and sys.argv[1] == '--scheduled':
        # Scheduled mode - run continuously
        automation.run_scheduled()
    else:
        # Default: run once
        print("Usage:")
        print("  python main.py --test      # Run once (test mode)")
        print("  python main.py --scheduled # Run with scheduler (production)")
        print("\nRunning in test mode...\n")
        automation.run_once()

if __name__ == "__main__":
    main()

