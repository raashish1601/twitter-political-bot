"""
Mention Handler Module - Adds relevant @mentions to tweets for maximum controversy and engagement
"""
import re
from typing import List, Set

class MentionHandler:
    def __init__(self):
        # Mapping of keywords to Twitter handles for maximum controversy
        # Format: {keyword: [list of handles]}
        self.mention_map = {
            # BJP/NDA Leaders
            'modi': ['@narendramodi', '@PMOIndia'],
            'narendra modi': ['@narendramodi', '@PMOIndia'],
            'yogi': ['@myogiadityanath', '@UPGovt'],
            'yogi adityanath': ['@myogiadityanath', '@UPGovt'],
            'amit shah': ['@AmitShah', '@HMOIndia'],
            'shah': ['@AmitShah'],
            'bjp': ['@BJP4India', '@BJP4India'],
            'nda': ['@BJP4India'],
            
            # Congress/Opposition Leaders
            'rahul gandhi': ['@RahulGandhi', '@INCIndia'],
            'rahul': ['@RahulGandhi', '@INCIndia'],
            'congress': ['@INCIndia', '@RahulGandhi'],
            'sonia gandhi': ['@INCIndia'],
            'priyanka gandhi': ['@priyankagandhi', '@INCIndia'],
            
            # AAP
            'kejriwal': ['@ArvindKejriwal', '@AamAadmiParty'],
            'aap': ['@AamAadmiParty', '@ArvindKejriwal'],
            'delhi': ['@ArvindKejriwal', '@AamAadmiParty'],
            
            # TMC
            'mamata': ['@MamataOfficial', '@AITCofficial'],
            'mamata banerjee': ['@MamataOfficial', '@AITCofficial'],
            'tmc': ['@AITCofficial', '@MamataOfficial'],
            'west bengal': ['@MamataOfficial', '@AITCofficial'],
            'bengal': ['@MamataOfficial'],
            
            # Other Politicians
            'nitish kumar': ['@NitishKumar'],
            'lalu': ['@laluprasadrjd'],
            'mulayam': ['@yadavakhilesh'],
            'akhilesh': ['@yadavakhilesh'],
            'mayawati': ['@Mayawati'],
            'uddhav': ['@OfficeofUT'],
            
            # Stock Market
            'nifty': ['@NSEIndia', '@BSEIndia'],
            'sensex': ['@BSEIndia', '@NSEIndia'],
            'stock market': ['@NSEIndia', '@BSEIndia'],
            'sebi': ['@SEBI_India'],
            'ipo': ['@NSEIndia', '@BSEIndia'],
            'fii': ['@NSEIndia'],
            'dii': ['@NSEIndia'],
            
            # News Outlets (for controversy)
            'republic': ['@republic'],
            'aaj tak': ['@aajtak'],
            'times now': ['@TimesNow'],
            'ndtv': ['@ndtv'],
            'india today': ['@IndiaToday'],
            'the wire': ['@thewire_in'],
            'scroll': ['@scroll_in'],
            
            # General Political Terms
            'election': ['@ECISVEEP'],
            'elections': ['@ECISVEEP'],
            'poll': ['@ECISVEEP'],
        }
        
        # Controversy-focused handles (always add for maximum engagement)
        self.controversy_handles = [
            '@RahulGandhi',  # Tag opposition for BJP tweets
            '@INCIndia',
            '@AamAadmiParty',
            '@AITCofficial',
        ]
    
    def extract_mentions(self, text: str, is_stock_market: bool = False) -> List[str]:
        """
        Extract relevant Twitter handles based on tweet content
        Returns list of handles to mention
        """
        text_lower = text.lower()
        mentions = []
        seen_handles = set()
        
        # Check for keywords in the text
        for keyword, handles in self.mention_map.items():
            if keyword in text_lower:
                for handle in handles:
                    if handle not in seen_handles:
                        mentions.append(handle)
                        seen_handles.add(handle)
                        # Limit to 3-4 mentions max to avoid spam
                        if len(mentions) >= 4:
                            break
                if len(mentions) >= 4:
                    break
        
        # For political tweets, add controversy handles strategically
        if not is_stock_market and len(mentions) < 3:
            # Add opposition handles if BJP/Modi is mentioned (creates controversy)
            if any(kw in text_lower for kw in ['modi', 'bjp', 'nda', 'yogi', 'shah']):
                for handle in self.controversy_handles[:2]:
                    if handle not in seen_handles and len(mentions) < 4:
                        mentions.append(handle)
                        seen_handles.add(handle)
        
        # For stock market tweets, add relevant handles
        if is_stock_market and len(mentions) < 2:
            if any(kw in text_lower for kw in ['nifty', 'sensex', 'stock', 'market']):
                if '@NSEIndia' not in seen_handles:
                    mentions.append('@NSEIndia')
                if '@BSEIndia' not in seen_handles and len(mentions) < 3:
                    mentions.append('@BSEIndia')
        
        return mentions[:4]  # Max 4 mentions per tweet
    
    def add_mentions_to_tweet(self, tweet_text: str, is_stock_market: bool = False) -> str:
        """
        Add relevant @mentions to a tweet for maximum controversy and engagement
        Ensures tweet stays under 280 characters
        """
        # Extract mentions
        mentions = self.extract_mentions(tweet_text, is_stock_market)
        
        if not mentions:
            return tweet_text
        
        # Calculate space needed for mentions
        mentions_text = ' ' + ' '.join(mentions)
        mentions_length = len(mentions_text)
        
        # Check if we can add mentions without exceeding limit
        current_length = len(tweet_text)
        total_length = current_length + mentions_length
        
        if total_length <= 280:
            # Simple case: just append mentions
            return tweet_text + mentions_text
        else:
            # Need to trim tweet to fit mentions
            available_space = 280 - mentions_length - 3  # -3 for "..."
            
            if available_space < 50:  # Too little space, don't add mentions
                return tweet_text
            
            # Trim tweet and add mentions
            trimmed_tweet = tweet_text[:available_space].rsplit(' ', 1)[0]  # Cut at word boundary
            return trimmed_tweet + "..." + mentions_text
    
    def get_controversy_mentions(self, topic_type: str = 'politics') -> List[str]:
        """
        Get handles that create maximum controversy based on topic type
        """
        if topic_type == 'politics':
            # Tag both sides for maximum controversy
            return ['@RahulGandhi', '@BJP4India']
        elif topic_type == 'stock_market':
            return ['@NSEIndia', '@BSEIndia']
        else:
            return ['@INCIndia', '@BJP4India']

