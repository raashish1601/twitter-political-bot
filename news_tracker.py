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
    
    def _extract_topic(self, title, description=None):
        """
        Extract main topic/subject from article title and description
        Returns a normalized topic string for comparison
        """
        if not title:
            return ""
        
        # Combine title and description
        text = title
        if description:
            text = f"{title} {description}"
        
        # Normalize
        text = self._normalize_text(text)
        
        # Remove common words and extract key entities
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how', 'about', 'into', 'through', 'during', 'including', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'including', 'against', 'among', 'throughout', 'despite', 'towards', 'upon', 'concerning', 'india', 'indian'}
        
        # Extract meaningful words (nouns, proper nouns, key terms)
        words = text.split()
        # Keep words that are:
        # - Longer than 3 characters
        # - Not in stop words
        # - Capitalized (likely proper nouns) or important keywords
        key_words = []
        for word in words:
            word_clean = word.strip('.,!?;:()[]{}"\'').lower()
            if len(word_clean) > 3 and word_clean not in stop_words:
                key_words.append(word_clean)
        
        # Return top 5-7 key words as topic signature
        return ' '.join(sorted(set(key_words))[:7])
    
    def _extract_topic_from_tweet(self, tweet_text):
        """
        Extract main topic from tweet text (removing hashtags and common words)
        """
        if not tweet_text:
            return ""
        
        # Remove hashtags for topic extraction
        words = tweet_text.split()
        content_words = [w for w in words if not w.startswith('#') and not w.startswith('@')]
        text = ' '.join(content_words)
        
        # Normalize and extract key words
        return self._extract_topic(text)
    
    def is_already_posted(self, article_url, article_title=None, tweet_text=None, description=None):
        """
        Check if an article/topic has already been posted
        Uses multiple checks: URL, title similarity, topic extraction, and tweet content similarity
        """
        # Check 1: Exact URL match
        if article_url:
            for item in self.posted_news:
                if item.get('url') == article_url:
                    print(f"🚫 Duplicate detected: Same URL already posted")
                    return True
        
        # Check 2: Extract and compare topics (most important - ensures different topics)
        current_topic = None
        if article_title:
            current_topic = self._extract_topic(article_title, description)
        
        if current_topic:
            for item in self.posted_news:
                # Get topic from stored item
                stored_topic = item.get('topic', '')
                if not stored_topic and item.get('title'):
                    # Extract topic from stored title if not already stored
                    stored_topic = self._extract_topic(item.get('title', ''), item.get('description', ''))
                
                if stored_topic and current_topic:
                    # Compare topics - if they share significant keywords, it's the same topic
                    current_words = set(current_topic.split())
                    stored_words = set(stored_topic.split())
                    
                    # Calculate overlap
                    if len(current_words) > 0 and len(stored_words) > 0:
                        overlap = len(current_words & stored_words)
                        total_unique = len(current_words | stored_words)
                        topic_similarity = overlap / total_unique if total_unique > 0 else 0
                        
                        # If 60%+ of keywords overlap, it's the same topic
                        if topic_similarity > 0.60:
                            print(f"🚫 Duplicate detected: Same topic already posted ({(topic_similarity*100):.1f}% topic overlap)")
                            print(f"   Previous topic: {stored_topic[:80]}...")
                            print(f"   Current topic:  {current_topic[:80]}...")
                            return True
        
        # Check 3: Title similarity (catch same story from different sources)
        if article_title:
            normalized_title = self._normalize_text(article_title)
            for item in self.posted_news:
                posted_title = self._normalize_text(item.get('title', ''))
                if posted_title and len(normalized_title) > 20:  # Only check if title is substantial
                    similarity = self._similarity_score(normalized_title, posted_title)
                    if similarity > 0.75:  # Lowered to 75% to catch more duplicates
                        print(f"🚫 Duplicate detected: Similar title ({(similarity*100):.1f}% match)")
                        print(f"   Previous: {item.get('title', '')[:60]}...")
                        print(f"   Current:  {article_title[:60]}...")
                        return True
        
        # Check 4: Tweet content topic extraction (avoid posting about same topic with different wording)
        if tweet_text:
            tweet_topic = self._extract_topic_from_tweet(tweet_text)
            if tweet_topic:
                for item in self.posted_news:
                    if item.get('tweet_text'):
                        posted_tweet_topic = self._extract_topic_from_tweet(item.get('tweet_text', ''))
                        if posted_tweet_topic:
                            current_words = set(tweet_topic.split())
                            posted_words = set(posted_tweet_topic.split())
                            
                            if len(current_words) > 0 and len(posted_words) > 0:
                                overlap = len(current_words & posted_words)
                                total_unique = len(current_words | posted_words)
                                topic_similarity = overlap / total_unique if total_unique > 0 else 0
                                
                                if topic_similarity > 0.60:
                                    print(f"🚫 Duplicate detected: Same topic in tweet ({(topic_similarity*100):.1f}% topic overlap)")
                                    return True
        
        return False
    
    def mark_as_posted(self, article_url, article_title, tweet_id, tweet_text=None, description=None):
        """
        Mark an article as posted (including tweet text and topic for duplicate checking)
        """
        # Extract topic for tracking
        topic = self._extract_topic(article_title, description)
        if not topic and tweet_text:
            topic = self._extract_topic_from_tweet(tweet_text)
        
        self.posted_news.append({
            'url': article_url,
            'title': article_title,
            'description': description,  # Store description for topic extraction
            'tweet_id': tweet_id,
            'tweet_text': tweet_text,  # Store tweet text for duplicate checking
            'topic': topic,  # Store extracted topic to prevent same topic posts
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

