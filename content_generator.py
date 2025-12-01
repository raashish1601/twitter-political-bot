"""
Content Generator Module - Creates funky, witty tweets using OpenAI
"""
import openai
import os
import re
import random
from dotenv import load_dotenv

load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.use_openai = bool(self.openai_api_key and self.openai_api_key.strip())
        
        if self.use_openai:
            try:
                openai.api_key = self.openai_api_key
                self.client = openai.OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                print(f"⚠️  OpenAI initialization failed: {e}")
                self.use_openai = False
        else:
            print("⚠️  OpenAI API key not found, will use fallback tweet generator")
            self.use_openai = False
        
    def generate_funky_tweet(self, news_article, trending_topics=None, is_stock_market=False):
        """
        Generate a funky, controversial tweet - political or stock market
        """
        title = news_article.get('title', '')
        description = news_article.get('description', '') or title
        source = news_article.get('source', '')
        
        # Build trending context
        trending_context = ""
        if trending_topics:
            relevant_trends = [t for t in trending_topics[:5] if not t.startswith('#')]
            if relevant_trends:
                trending_context = f"\n\nCurrent Twitter trends to consider: {', '.join(relevant_trends[:3])}"
        
        # Check if OpenAI is available, otherwise use fallback directly
        if not self.use_openai:
            return self._create_fallback_tweet(news_article, trending_topics, is_stock_market)
        
        if is_stock_market:
            prompt = f"""Create a CONTROVERSIAL, FUNKY Twitter post (max 280 characters) about this Indian stock market news that will CREATE DEBATE and CONTROVERSY.
        
News: {title}
Description: {description}{trending_context}

Requirements:
- MUST CREATE CONTROVERSY - challenge popular opinions, expose hidden truths, question mainstream narratives
- EXTREMELY funky, witty, and provocative - make people think and debate
- Use bold statements, contrarian takes, expose market manipulation or insider trading hints
- Question broker recommendations, expose FII/DII games, challenge market gurus
- Create FOMO or fear - make people question their investments
- Use savage humor, brutal sarcasm about market crashes, pump & dump schemes
- PRIORITY: Include TOP TRENDING hashtags for maximum reach
- Make it VIRAL-worthy - controversial tweets get more engagement!
- Keep it under 280 characters
- Be clever, funky, and absolutely CONTROVERSIAL - make people angry, debate, share!

Generate ONLY the tweet text with trending hashtags prioritized, nothing else:"""
            
            system_prompt = "You are a CONTROVERSIAL, FUNKY financial content creator who creates absolutely BRUTAL, provocative stock market tweets that CREATE DEBATE. You expose market manipulation, question mainstream narratives, challenge broker recommendations, and create controversy. You're funky, witty, and make people think critically about the market. Your tweets are designed to go viral through controversy and debate."
        else:
            prompt = f"""Create a CONTROVERSIAL, FUNKY Twitter post (max 280 characters) about this Indian political news that will CREATE DEBATE and CONTROVERSY.
        
News: {title}
Description: {description}{trending_context}

Requirements:
- MUST CREATE CONTROVERSY - challenge narratives, expose truths, question everything
- Pro-BJP/NDA bias, EXTREMELY funky and witty
- BURN the opposition with clever, sarcastic, funky roasts (can be spicy/offensive but in a funky way)
- Use savage humor, brutal sarcasm, clever wordplay - make opposition look foolish
- Expose corruption, question policies, create debate on sensitive issues
- NO emotional drama - pure funky, savage wit with controversy
- PRIORITY: Include TOP TRENDING hashtags for maximum reach (even if loosely related)
- Incorporate trending topics naturally into the tweet
- Make it VIRAL-worthy and shareable - controversial tweets get more engagement!
- Keep it under 280 characters
- Be clever, funky, and absolutely CONTROVERSIAL - make people angry, debate, share!

Generate ONLY the tweet text with trending hashtags prioritized, nothing else:"""
            
            system_prompt = "You are a CONTROVERSIAL, FUNKY social media content creator who creates absolutely BRUTAL, provocative political tweets with a pro-BJP/NDA bias. You CREATE CONTROVERSY by challenging narratives, exposing truths, and making people debate. You BURN opposition with savage humor, brutal sarcasm, and clever wordplay. You're funky, witty, and make opposition look absolutely foolish. Your tweets are designed to go viral through controversy and debate."

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.98  # Increased for more creativity and controversy
            )
            
            tweet = response.choices[0].message.content.strip()
            
            # Clean up the tweet (remove quotes if wrapped)
            if tweet.startswith('"') and tweet.endswith('"'):
                tweet = tweet[1:-1]
            if tweet.startswith("'") and tweet.endswith("'"):
                tweet = tweet[1:-1]
            
            # Ensure it's under 280 characters
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            return tweet
            
        except Exception as e:
            error_msg = str(e)
            # Check for specific error types
            if 'authentication' in error_msg.lower() or 'invalid api key' in error_msg.lower() or '401' in error_msg:
                print("❌ OpenAI API key is invalid or missing. Using fallback tweet generator.")
                self.use_openai = False  # Disable OpenAI for future calls
            elif 'rate limit' in error_msg.lower() or '429' in error_msg or 'quota' in error_msg.lower():
                print("⚠️  OpenAI rate limit/quota exceeded. Using fallback tweet generator.")
            elif '404' in error_msg or 'model' in error_msg.lower():
                print("⚠️  OpenAI model not found. Using fallback tweet generator.")
            else:
                print(f"⚠️  OpenAI API error: {error_msg[:100]}. Using fallback tweet generator.")
            
            return self._create_fallback_tweet(news_article, trending_topics, is_stock_market)
    
    def _create_fallback_tweet(self, news_article, trending_topics=None, is_stock_market=False):
        """
        Create a funky, controversial tweet if AI generation fails
        """
        title = news_article.get('title', '')
        description = news_article.get('description', '') or title
        text = title if len(title) < 180 else description[:180]
        
        # Generate relevant hashtags from content
        hashtags = self._generate_relevant_hashtags(text, trending_topics, is_stock_market)
        
        text_lower = text.lower()
        
        if is_stock_market:
            # Controversial stock market intros
            controversial_intros = [
                "🚨 Market manipulation alert! 💸\n\n",
                "⚠️ Someone's getting rich while you sleep... 😏\n\n",
                "🔥 The truth they don't want you to know:\n\n",
                "💀 Market gurus exposed again... 😂\n\n",
                "⚡ FII/DII playing games? You decide... 🤔\n\n",
                "🎯 Insider trading vibes? 🤷\n\n"
            ]
            funky_intro = random.choice(controversial_intros)
        else:
            # Controversial political intros
            opposition_keywords = ['congress', 'rahul', 'opposition', 'alliance', 'aap', 'tmc', 'kejriwal', 'mamata']
            bjp_keywords = ['bjp', 'nda', 'modi', 'yogi', 'shah']
            
            if any(kw in text_lower for kw in opposition_keywords):
                funky_intros = [
                    "🚨 Opposition exposed again! 😂 BJP keeps winning! 🔥\n\n",
                    "💀 Another L for opposition... Meanwhile development continues! 😏\n\n",
                    "⚡ Opposition: *exists* \nBJP: *wins* \nThe truth hurts! 💪\n\n",
                    "🔥 Opposition doing mental gymnastics while BJP delivers... Facts! 🚀\n\n"
                ]
                funky_intro = random.choice(funky_intros)
            elif any(kw in text_lower for kw in bjp_keywords):
                funky_intros = [
                    "🚀 Another W for development! Opposition seething! 🔥\n\n",
                    "💪 BJP delivering as usual! Facts don't care about feelings! 🎯\n\n",
                    "🔥 Modi ji at it again! Development > Drama! ⚡\n\n"
                ]
                funky_intro = random.choice(funky_intros)
            else:
                funky_intro = "🚨 Latest from Indian politics (the truth they hide): 💪\n\n"
        
        # Calculate available space
        available = 280 - len(funky_intro) - len(hashtags) - 5
        
        if len(text) > available:
            text = text[:available-3] + "..."
        
        tweet = f"{funky_intro}{text}\n\n{hashtags}"
        
        # Ensure it's under 280
        if len(tweet) > 280:
            # Trim hashtags if needed
            if len(tweet) > 280:
                excess = len(tweet) - 280
                hashtags = hashtags[:-excess-3] + "..."
                tweet = f"{funky_intro}{text}\n\n{hashtags}"
        
        return tweet
    
    def _generate_relevant_hashtags(self, text, trending_topics=None, is_stock_market=False):
        """
        Generate relevant hashtags with TRENDING PRIORITY for maximum reach
        """
        text_lower = text.lower()
        hashtags = []
        
        # PRIORITY 1: Add TOP TRENDING hashtags (for maximum reach)
        if trending_topics:
            # Always include top 2-3 trending hashtags (even if not directly related)
            trending_hashtags = []
            for trend in trending_topics[:5]:
                if trend.startswith('#'):
                    # It's already a hashtag
                    if trend not in hashtags:
                        trending_hashtags.append(trend)
                else:
                    # Convert to hashtag (remove spaces, special chars)
                    trend_hashtag = '#' + ''.join(c for c in trend if c.isalnum() or c == ' ')
                    trend_hashtag = trend_hashtag.replace(' ', '')
                    if trend_hashtag not in hashtags and len(trend_hashtag) > 1:
                        trending_hashtags.append(trend_hashtag)
            
            # Add top 2-3 trending hashtags FIRST (for maximum reach)
            hashtags.extend(trending_hashtags[:3])
        
        if is_stock_market:
            # Stock market hashtags
            if 'nifty' in text_lower or 'nse' in text_lower:
                hashtags.append('#Nifty')
            if 'sensex' in text_lower or 'bse' in text_lower:
                hashtags.append('#Sensex')
            if 'ipo' in text_lower:
                hashtags.append('#IPO')
            if 'stock' in text_lower or 'share' in text_lower:
                hashtags.append('#StockMarket')
            if 'invest' in text_lower or 'investor' in text_lower:
                hashtags.append('#Investing')
            if 'fii' in text_lower or 'dii' in text_lower:
                hashtags.append('#FII')
            if 'crash' in text_lower or 'fall' in text_lower or 'drop' in text_lower:
                hashtags.append('#MarketCrash')
            if 'bull' in text_lower or 'rally' in text_lower:
                hashtags.append('#BullRun')
            
            # Always add stock market related
            if '#StockMarket' not in ' '.join(hashtags):
                hashtags.append('#StockMarket')
        else:
            # PRIORITY 2: Content-relevant political party hashtags
            if 'bjp' in text_lower or 'modi' in text_lower or 'nda' in text_lower:
                if '#BJP' not in ' '.join(hashtags):
                    hashtags.append('#BJP')
                if '#NDA' not in ' '.join(hashtags):
                    hashtags.append('#NDA')
            if 'congress' in text_lower or 'rahul' in text_lower:
                if '#Congress' not in ' '.join(hashtags):
                    hashtags.append('#Congress')
            if 'aap' in text_lower or 'kejriwal' in text_lower:
                if '#AAP' not in ' '.join(hashtags):
                    hashtags.append('#AAP')
            if 'tmc' in text_lower or 'mamata' in text_lower:
                if '#TMC' not in ' '.join(hashtags):
                    hashtags.append('#TMC')
            
            # PRIORITY 3: Topic-based hashtags (if space available)
            if len(hashtags) < 5:
                if 'west bengal' in text_lower or 'bengal' in text_lower:
                    hashtags.append('#WestBengal')
                if 'delhi' in text_lower:
                    hashtags.append('#Delhi')
                if 'election' in text_lower or 'poll' in text_lower:
                    hashtags.append('#Elections')
                if 'development' in text_lower or 'growth' in text_lower:
                    hashtags.append('#Development')
                if 'infiltration' in text_lower or 'immigration' in text_lower:
                    hashtags.append('#NationalSecurity')
        
        # PRIORITY 4: Always add India (if space)
        if '#India' not in ' '.join(hashtags) and len(hashtags) < 6:
            hashtags.append('#India')
        
        # Limit to 5-6 hashtags max (Twitter best practice)
        return ' '.join(hashtags[:6])

