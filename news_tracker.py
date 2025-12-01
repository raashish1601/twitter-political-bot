"""
News Tracker Module - Tracks posted news to avoid duplicates
"""
import json
import os
from datetime import datetime
from difflib import SequenceMatcher

class NewsTracker:
    def __init__(self, storage_file='posted_news.json'):
        self.storage_file = storage_file
        self.posted_news = self._load_posted_news()
    
    def _load_posted_news(self):
        """
        Load previously posted news from file
        """
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_posted_news(self):
        """
        Save posted news to file
        """
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.posted_news, f, indent=2)
        except Exception as e:
            print(f"Error saving posted news: {e}")
    
    def _normalize_text(self, text):
        """
        Normalize text for comparison (lowercase, remove extra spaces)
        """
        if not text:
            return ""
        return " ".join(text.lower().split())
    
    def _similarity_score(self, text1, text2):
        """
        Calculate similarity score between two texts (0-1)
        """
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def is_already_posted(self, article_url, article_title=None, tweet_text=None):
        """
        Check if an article has already been posted
        Uses multiple checks: URL, title similarity, and tweet content similarity
        """
        # Check 1: Exact URL match
        if article_url:
            for item in self.posted_news:
                if item.get('url') == article_url:
                    print(f"🚫 Duplicate detected: Same URL already posted")
                    return True
        
        # Check 2: Title similarity (catch same story from different sources)
        if article_title:
            normalized_title = self._normalize_text(article_title)
            for item in self.posted_news:
                posted_title = self._normalize_text(item.get('title', ''))
                if posted_title and len(normalized_title) > 20:  # Only check if title is substantial
                    similarity = self._similarity_score(normalized_title, posted_title)
                    if similarity > 0.85:  # 85% similarity threshold
                        print(f"🚫 Duplicate detected: Similar title ({(similarity*100):.1f}% match)")
                        print(f"   Previous: {item.get('title', '')[:60]}...")
                        print(f"   Current:  {article_title[:60]}...")
                        return True
        
        # Check 3: Tweet content similarity (avoid posting similar tweets)
        if tweet_text:
            normalized_tweet = self._normalize_text(tweet_text)
            # Extract main content (remove hashtags for comparison)
            tweet_content = ' '.join([w for w in normalized_tweet.split() if not w.startswith('#')])
            
            for item in self.posted_news:
                if item.get('tweet_text'):
                    posted_tweet = self._normalize_text(item.get('tweet_text', ''))
                    posted_content = ' '.join([w for w in posted_tweet.split() if not w.startswith('#')])
                    
                    if len(tweet_content) > 50 and len(posted_content) > 50:
                        similarity = self._similarity_score(tweet_content, posted_content)
                        if similarity > 0.80:  # 80% similarity threshold for tweet content
                            print(f"🚫 Duplicate detected: Similar tweet content ({(similarity*100):.1f}% match)")
                            return True
        
        return False
    
    def mark_as_posted(self, article_url, article_title, tweet_id, tweet_text=None):
        """
        Mark an article as posted (including tweet text for duplicate checking)
        """
        self.posted_news.append({
            'url': article_url,
            'title': article_title,
            'tweet_id': tweet_id,
            'tweet_text': tweet_text,  # Store tweet text for duplicate detection
            'posted_at': datetime.now().isoformat()
        })
        self._save_posted_news()
    
    def cleanup_old_entries(self, days=30):
        """
        Remove entries older than specified days (increased to 30 days for better duplicate prevention)
        """
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            original_count = len(self.posted_news)
            self.posted_news = [
                item for item in self.posted_news
                if datetime.fromisoformat(item['posted_at']).timestamp() > cutoff_date
            ]
            
            removed = original_count - len(self.posted_news)
            if removed > 0:
                print(f"🧹 Cleaned up {removed} old entries (older than {days} days)")
                self._save_posted_news()
        except Exception as e:
            print(f"⚠️  Error during cleanup: {e}")

