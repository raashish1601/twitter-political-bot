"""
News Fetcher Module - Fetches latest Indian political news
"""
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class NewsFetcher:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2/everything'
        
    def fetch_latest_news(self, max_results=10):
        """
        Fetch latest Indian political news with BJP/NDA focus
        """
        # Keywords for BJP/NDA and Indian politics
        query = '(BJP OR NDA OR Modi OR "Prime Minister" OR "Indian politics" OR Congress OR opposition) AND India'
        
        # Get news from last 24 hours
        from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': max_results,
            'from': from_date,
            'apiKey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                
                # Filter and prioritize BJP/NDA related news
                prioritized_articles = self._prioritize_articles(articles)
                
                return prioritized_articles[:5]  # Return top 5
            else:
                print(f"News API error: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
    
    def _prioritize_articles(self, articles):
        """
        Prioritize articles with BJP/NDA keywords
        """
        bjp_keywords = ['BJP', 'NDA', 'Modi', 'PM Modi', 'Bharatiya Janata Party', 
                       'Yogi', 'Shah', 'Narendra Modi']
        opposition_keywords = ['Congress', 'Rahul Gandhi', 'AAP', 'TMC', 
                              'opposition', 'alliance']
        
        prioritized = []
        regular = []
        
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower() if article.get('description') else ''
            content = title + ' ' + description
            
            # Check if BJP/NDA related
            if any(keyword.lower() in content for keyword in bjp_keywords):
                # Check if also mentions opposition (good for funky tweets)
                if any(keyword.lower() in content for keyword in opposition_keywords):
                    prioritized.insert(0, article)  # Highest priority
                else:
                    prioritized.append(article)
            elif any(keyword.lower() in content for keyword in opposition_keywords):
                regular.append(article)
            else:
                regular.append(article)
        
        return prioritized + regular
    
    def prioritize_by_trends(self, articles, trending_topics):
        """
        Re-prioritize articles based on trending topics for maximum reach
        """
        if not trending_topics:
            return articles
        
        # Extract keywords from trending topics (remove # and common words)
        trend_keywords = []
        for trend in trending_topics:
            # Remove # and split into words
            trend_clean = trend.replace('#', '').lower()
            words = trend_clean.split()
            # Add meaningful words (length > 3)
            trend_keywords.extend([w for w in words if len(w) > 3])
        
        # Score articles based on trend matches
        scored_articles = []
        for article in articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower() if article.get('description') else ''
            content = title + ' ' + description
            
            # Calculate trend match score
            trend_score = 0
            for keyword in trend_keywords:
                if keyword in content:
                    trend_score += 2  # High weight for trend matches
            
            # Also check if trend itself appears
            for trend in trending_topics[:5]:  # Top 5 trends
                trend_clean = trend.replace('#', '').lower()
                if trend_clean in content or any(word in content for word in trend_clean.split() if len(word) > 3):
                    trend_score += 5  # Very high weight for direct trend match
            
            scored_articles.append((trend_score, article))
        
        # Sort by trend score (highest first)
        scored_articles.sort(key=lambda x: x[0], reverse=True)
        
        # Return reordered articles
        return [article for score, article in scored_articles]
    
    def get_article_summary(self, article):
        """
        Extract key information from article
        """
        return {
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'url': article.get('url', ''),
            'source': article.get('source', {}).get('name', ''),
            'published_at': article.get('publishedAt', ''),
            'image_url': article.get('urlToImage', '')  # Add image URL
        }

