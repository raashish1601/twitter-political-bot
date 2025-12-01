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
            
            # Major Indian Companies (Stock Market)
            'reliance': ['@reliancejio', '@RIL_Updates'],
            'tata': ['@TataCompanies', '@TataMotors'],
            'infosys': ['@Infosys'],
            'tcs': ['@TCS'],
            'wipro': ['@Wipro'],
            'hdfc': ['@HDFCBank', '@HDFC_Bank'],
            'icici': ['@ICICIBank'],
            'sbi': ['@TheOfficialSBI'],
            'axis bank': ['@AxisBank'],
            'hdfc bank': ['@HDFCBank'],
            'hul': ['@HUL_News'],
            'hindustan unilever': ['@HUL_News'],
            'itc': ['@ITCCorpCom'],
            'bharti airtel': ['@Airtel_Presence'],
            'airtel': ['@Airtel_Presence'],
            'adani': ['@AdaniOnline'],
            'adani group': ['@AdaniOnline'],
            'zomato': ['@zomato'],
            'swiggy': ['@Swiggy'],
            'paytm': ['@Paytm'],
            'nykaa': ['@Nykaa'],
            'houselane': ['@HomeLane'],
            'homelane': ['@HomeLane'],
            'byju': ['@BYJUS'],
            'byjus': ['@BYJUS'],
            'ola': ['@Olacabs'],
            'uber': ['@Uber_India'],
            'flipkart': ['@Flipkart'],
            'amazon': ['@amazonIN'],
            'jio': ['@reliancejio'],
            'vi': ['@VodafoneIN'],
            'vodafone idea': ['@VodafoneIN'],
            
            # Stock Market Brokers/Analysts
            'zerodha': ['@zerodhaonline'],
            'groww': ['@_groww'],
            'upstox': ['@Upstox'],
            'angel one': ['@AngelOneIN'],
            'icici direct': ['@ICICIDirect'],
            'hdfc securities': ['@HDFCSecurities'],
            'kotak securities': ['@KotakSec'],
            'motilal oswal': ['@MotilalOswal'],
            'sharekhan': ['@Sharekhan'],
            '5paisa': ['@5paisa'],
            
            # Business/Finance Personalities
            'mukesh ambani': ['@MukeshAmbani'],
            'ratan tata': ['@RNTata2000'],
            'gautam adani': ['@gautam_adani'],
            'nandan nilekani': ['@NandanNilekani'],
            'narayana murthy': ['@Infosys_nmurthy'],
            'rakesh jhunjhunwala': ['@RakeshJhunjhun'],
            'radhakishan damani': ['@DMartIndia'],
            
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
    
    def extract_mentions(self, text: str, is_stock_market: bool = False, article_title: str = None, article_description: str = None) -> List[str]:
        """
        Extract relevant Twitter handles based on tweet content
        Uses both tweet text and original article for better context
        Returns list of handles to mention
        """
        text_lower = text.lower()
        mentions = []
        seen_handles = set()
        
        # Combine tweet and article context for better extraction
        full_context = text_lower
        if article_title:
            full_context += " " + article_title.lower()
        if article_description:
            full_context += " " + article_description.lower()
        
        # Step 1: Check for keywords in the text (exact matches)
        for keyword, handles in self.mention_map.items():
            if keyword in full_context:
                for handle in handles:
                    if handle not in seen_handles:
                        mentions.append(handle)
                        seen_handles.add(handle)
                        # Limit to 3-4 mentions max to avoid spam
                        if len(mentions) >= 4:
                            break
                if len(mentions) >= 4:
                    break
        
        # Step 2: Extract company names dynamically (for stock market tweets)
        if is_stock_market:
            company_mentions = self._extract_company_mentions(full_context)
            for handle in company_mentions:
                if handle not in seen_handles and len(mentions) < 4:
                    mentions.append(handle)
                    seen_handles.add(handle)
        
        # Step 3: Extract CEO/founder names dynamically
        ceo_mentions = self._extract_ceo_mentions(full_context)
        for handle in ceo_mentions:
            if handle not in seen_handles and len(mentions) < 4:
                mentions.append(handle)
                seen_handles.add(handle)
        
        # Step 4: For political tweets, add controversy handles strategically
        if not is_stock_market and len(mentions) < 3:
            # Add opposition handles if BJP/Modi is mentioned (creates controversy)
            if any(kw in text_lower for kw in ['modi', 'bjp', 'nda', 'yogi', 'shah']):
                for handle in self.controversy_handles[:2]:
                    if handle not in seen_handles and len(mentions) < 4:
                        mentions.append(handle)
                        seen_handles.add(handle)
        
        # Step 5: For stock market tweets, add relevant handles if not enough
        if is_stock_market:
            # Add broker mentions if "broker" is mentioned
            if 'broker' in text_lower and len(mentions) < 4:
                broker_handles = ['@zerodhaonline', '@_groww', '@Upstox']
                for handle in broker_handles:
                    if handle not in seen_handles and len(mentions) < 4:
                        mentions.append(handle)
                        seen_handles.add(handle)
                        break
            
            # Add exchange mentions if not already present
            if len(mentions) < 3:
                if any(kw in text_lower for kw in ['nifty', 'sensex', 'stock', 'market', 'share', 'ipo', 'equity']):
                    if '@NSEIndia' not in seen_handles:
                        mentions.append('@NSEIndia')
                        seen_handles.add('@NSEIndia')
                    if '@BSEIndia' not in seen_handles and len(mentions) < 4:
                        mentions.append('@BSEIndia')
                        seen_handles.add('@BSEIndia')
        
        return mentions[:4]  # Max 4 mentions per tweet
    
    def _extract_company_mentions(self, text: str) -> List[str]:
        """
        Dynamically extract company names and find their Twitter handles
        """
        mentions = []
        
        # Pattern to find company names (capitalized words, often before keywords like 'stock', 'shares', 'IPO', etc.)
        # Look for patterns like "CompanyName stock", "CompanyName shares", "CompanyName IPO"
        company_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:stock|shares|ipo|equity|market|business|company|firm|corporation)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:announces|launches|reports|plans)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:CEO|founder|co-founder)',
            r'\'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\'',  # Quoted company names
            r'"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"',  # Quoted company names
        ]
        
        companies_found = set()
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ""
                if match and len(match) > 2:
                    companies_found.add(match.strip())
        
        # Also extract standalone capitalized words that might be companies
        # (words that are capitalized and not common words)
        capitalized_words = re.findall(r'\b([A-Z][a-z]{3,})\b', text)
        common_words = {'India', 'Indian', 'Stock', 'Market', 'Share', 'News', 'Latest', 'Breaking', 'Update', 'Report', 'Says', 'Will', 'This', 'That', 'The', 'And', 'For', 'With', 'From', 'About', 'After', 'Before', 'During', 'Under', 'Over', 'Between', 'Among'}
        
        for word in capitalized_words:
            if word not in common_words and len(word) > 3:
                companies_found.add(word)
        
        # Try to find Twitter handles for extracted companies
        for company in list(companies_found)[:5]:  # Limit to top 5 companies
            company_lower = company.lower().replace(' ', '')
            
            # Check if we have a direct mapping
            if company_lower in self.mention_map:
                for handle in self.mention_map[company_lower]:
                    if handle not in mentions:
                        mentions.append(handle)
            else:
                # Try to construct a likely Twitter handle
                # Format: @CompanyName (remove spaces, special chars)
                handle = '@' + re.sub(r'[^a-zA-Z0-9]', '', company)
                # Only add if it looks reasonable (not too long, not generic)
                if len(handle) > 4 and len(handle) < 20 and handle.lower() not in ['@the', '@and', '@for', '@with']:
                    # Don't add constructed handles - they might not exist
                    # Instead, check if company name matches any known company
                    pass
        
        return mentions[:3]  # Max 3 company mentions
    
    def _extract_ceo_mentions(self, text: str) -> List[str]:
        """
        Extract CEO/founder names and find their Twitter handles
        """
        mentions = []
        
        # Pattern to find CEO/founder names
        # Look for patterns like "CEO Name", "founder Name", "Name, CEO"
        ceo_patterns = [
            r'(?:CEO|Founder|Co-founder|MD|Managing Director|Chairman)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+(?:CEO|Founder|Co-founder|MD|Managing Director|Chairman)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+(?:says|said|announces|launches)',
        ]
        
        names_found = set()
        for pattern in ceo_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if match and len(match.split()) >= 2:  # At least first and last name
                    names_found.add(match.strip())
        
        # Try to find Twitter handles for extracted names
        for name in list(names_found)[:3]:  # Limit to top 3 names
            name_lower = name.lower()
            
            # Check if we have a direct mapping
            if name_lower in self.mention_map:
                for handle in self.mention_map[name_lower]:
                    if handle not in mentions:
                        mentions.append(handle)
        
        return mentions[:2]  # Max 2 CEO mentions
    
    def add_mentions_to_tweet(self, tweet_text: str, is_stock_market: bool = False, mentions: List[str] = None) -> str:
        """
        Add relevant @mentions to a tweet for maximum controversy and engagement
        Ensures tweet stays under 280 characters and is always complete
        """
        from text_utils import ensure_complete_tweet, truncate_tweet_complete
        
        # FIRST: Ensure the base tweet is complete (fix any incomplete sentences)
        tweet_text = ensure_complete_tweet(tweet_text, max_length=280)
        
        # Use provided mentions or extract them
        if mentions is None:
            mentions = self.extract_mentions(tweet_text, is_stock_market)
        
        if not mentions:
            # No mentions to add, return the complete tweet
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
            available_space = 280 - mentions_length
            
            if available_space < 50:  # Too little space, don't add mentions
                return tweet_text
            
            # Trim tweet at sentence boundary to ensure completeness
            trimmed_tweet = truncate_tweet_complete(tweet_text, available_space)
            return trimmed_tweet + mentions_text
    
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

