"""
News Tracker Module - Tracks posted news to avoid duplicates
"""
import json
import os
from datetime import datetime

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
    
    def is_already_posted(self, article_url):
        """
        Check if an article has already been posted
        """
        return article_url in [item.get('url') for item in self.posted_news]
    
    def mark_as_posted(self, article_url, article_title, tweet_id):
        """
        Mark an article as posted
        """
        self.posted_news.append({
            'url': article_url,
            'title': article_title,
            'tweet_id': tweet_id,
            'posted_at': datetime.now().isoformat()
        })
        self._save_posted_news()
    
    def cleanup_old_entries(self, days=7):
        """
        Remove entries older than specified days
        """
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        self.posted_news = [
            item for item in self.posted_news
            if datetime.fromisoformat(item['posted_at']).timestamp() > cutoff_date
        ]
        self._save_posted_news()

