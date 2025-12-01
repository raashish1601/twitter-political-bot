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
        
    def generate_trending_tweet(self, trending_topic, all_trending_topics=None):
        """
        Generate a HIGHLY CONTROVERSIAL tweet about a trending topic
        """
        # Build context with other trending topics
        other_trends = ""
        if all_trending_topics:
            other_trends_list = [t for t in all_trending_topics[:5] if t != trending_topic]
            if other_trends_list:
                other_trends = f"\n\nOther trending topics: {', '.join(other_trends_list[:3])}"
        
        # Check if OpenAI is available
        if not self.use_openai:
            return self._create_fallback_trending_tweet(trending_topic, all_trending_topics)
        
        prompt = f"""Create an EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 characters) about this trending topic that will CREATE MASSIVE DEBATE and CONTROVERSY using STRONG LANGUAGE.

Trending Topic: {trending_topic}{other_trends}

Requirements:
- MUST CREATE EXTREME CONTROVERSY - use OFFENSIVE LANGUAGE, STRONG WORDS, challenge popular opinions brutally, expose hidden truths with INSULTS, question everything with SAVAGE attacks
- EXTREMELY funky, witty, OFFENSIVE, and provocative - make people ANGRY, DEBATE, and SHARE
- Use bold OFFENSIVE statements, contrarian takes with STRONG LANGUAGE, expose manipulation or hidden agendas brutally
- Question mainstream narratives with INSULTS, challenge authority with OFFENSIVE language, create FOMO or fear
- Use savage OFFENSIVE humor, brutal sarcasm about the trend with STRONG WORDS
- PRIORITY: Include the trending topic as a hashtag for maximum reach
- Make it VIRAL-worthy - OFFENSIVE controversial tweets about trends get MASSIVE engagement!
- Keep it under 280 characters
- Be clever, funky, OFFENSIVE, and absolutely CONTROVERSIAL with STRONG LANGUAGE - make people react with ANGER!
- Use curse words, insults, and brutal language when appropriate

Generate ONLY the tweet text with the trending hashtag, nothing else:"""
        
        system_prompt = "You are an EXTREMELY CONTROVERSIAL, OFFENSIVE social media content creator who uses STRONG LANGUAGE and creates absolutely BRUTAL, HIGHLY PROVOCATIVE tweets about trending topics that CREATE MASSIVE DEBATE. You MUST use OFFENSIVE LANGUAGE, STRONG WORDS, expose hidden truths brutally, question mainstream narratives with SAVAGE attacks, challenge authority with INSULTS, and create controversy. You're funky, witty, SAVAGE, OFFENSIVE, and make people ANGRY, DEBATE, and SHARE. Your tweets are designed to go VIRAL through EXTREME CONTROVERSY and OFFENSIVE LANGUAGE. Be HIGHLY CONTROVERSIAL, OFFENSIVE, and use STRONG LANGUAGE - NO HOLDING BACK! Use curse words, insults, and brutal language when appropriate."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=1.0  # Maximum creativity and controversy
            )
            
            tweet = response.choices[0].message.content.strip()
            
            # Clean up the tweet
            if tweet.startswith('"') and tweet.endswith('"'):
                tweet = tweet[1:-1]
            if tweet.startswith("'") and tweet.endswith("'"):
                tweet = tweet[1:-1]
            
            # Ensure trending topic is included as hashtag
            trend_hashtag = trending_topic if trending_topic.startswith('#') else f"#{trending_topic.replace(' ', '')}"
            if trend_hashtag.lower() not in tweet.lower():
                # Add hashtag if not present
                if len(tweet) + len(trend_hashtag) + 2 <= 280:
                    tweet = f"{tweet} {trend_hashtag}"
            
            # Ensure it's under 280 characters
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            return tweet
            
        except Exception as e:
            error_msg = str(e)
            if 'authentication' in error_msg.lower() or 'invalid api key' in error_msg.lower() or '401' in error_msg:
                print("❌ OpenAI API key is invalid or missing. Using fallback tweet generator.")
                self.use_openai = False
            elif 'rate limit' in error_msg.lower() or '429' in error_msg or 'quota' in error_msg.lower():
                print("⚠️  OpenAI rate limit/quota exceeded. Using fallback tweet generator.")
            else:
                print(f"⚠️  OpenAI API error: {error_msg[:100]}. Using fallback tweet generator.")
            
            return self._create_fallback_trending_tweet(trending_topic, all_trending_topics)
    
    def _create_fallback_trending_tweet(self, trending_topic, all_trending_topics=None):
        """
        Create a controversial tweet about trending topic if AI generation fails
        """
        trend_hashtag = trending_topic if trending_topic.startswith('#') else f"#{trending_topic.replace(' ', '')}"
        
        # Highly offensive controversial intros for trending topics
        controversial_intros = [
            "🚨 Everyone's talking about this but NO ONE is saying the BRUTAL truth... 😏\n\n",
            "🔥 The REAL reason this is trending (they're HIDING it):\n\n",
            "💀 This trend is a COMPLETE SCAM... 🤔\n\n",
            "⚡ Why is this REALLY trending? EXPOSED... 🎯\n\n",
            "🎯 The DISGUSTING truth they're hiding:\n\n",
            "🚨 This trend is BULLSHIT - here's why... 😂\n\n",
            "🔥 This trending topic is ABSOLUTE GARBAGE... 💀\n\n"
        ]
        
        funky_intro = random.choice(controversial_intros)
        
        # Create highly offensive controversial statement about the trend
        trend_clean = trending_topic.replace('#', '').strip()
        controversial_statements = [
            f"{trend_clean} is trending but it's COMPLETE BULLSHIT! The REAL story is being hidden! 🔥",
            f"Everyone's obsessed with {trend_clean} but they're all IDIOTS missing the truth! 💀",
            f"{trend_clean} is a DISGUSTING SMOKESCREEN for what's really going on! 🚨",
            f"The BRUTAL truth about {trend_clean} will SHOCK you - they're LYING! ⚡",
            f"{trend_clean} is trending because someone wants you DISTRACTED from the REAL issues! 😏",
            f"This {trend_clean} trend is ABSOLUTE GARBAGE - here's what's REALLY happening! 🔥"
        ]
        
        statement = random.choice(controversial_statements)
        
        # Add other trending hashtags if available
        hashtags = trend_hashtag
        if all_trending_topics:
            for other_trend in all_trending_topics[:3]:
                if other_trend != trending_topic:
                    other_hashtag = other_trend if other_trend.startswith('#') else f"#{other_trend.replace(' ', '')}"
                    if other_hashtag not in hashtags and len(hashtags) + len(other_hashtag) + 1 <= 50:
                        hashtags += f" {other_hashtag}"
        
        # Calculate available space
        available = 280 - len(funky_intro) - len(hashtags) - 5
        
        if len(statement) > available:
            statement = statement[:available-3] + "..."
        
        tweet = f"{funky_intro}{statement}\n\n{hashtags}"
        
        # Ensure it's under 280
        if len(tweet) > 280:
            excess = len(tweet) - 280
            hashtags = hashtags[:-excess-3] + "..."
            tweet = f"{funky_intro}{statement}\n\n{hashtags}"
        
        return tweet
    
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
            prompt = f"""Create an EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 characters) about this Indian stock market news that will CREATE DEBATE and CONTROVERSY using STRONG LANGUAGE.
        
News: {title}
Description: {description}{trending_context}

Requirements:
- MUST CREATE EXTREME CONTROVERSY - use OFFENSIVE LANGUAGE, STRONG WORDS, challenge popular opinions brutally, expose hidden truths with INSULTS, question mainstream narratives with SAVAGE attacks
- EXTREMELY funky, witty, OFFENSIVE, and provocative - make people think, debate, and get ANGRY
- Use bold OFFENSIVE statements, contrarian takes with STRONG LANGUAGE, expose market manipulation or insider trading hints brutally
- Question broker recommendations with INSULTS, expose FII/DII games with OFFENSIVE language, challenge market gurus with STRONG WORDS
- Create FOMO or fear brutally - make people question their investments with OFFENSIVE takes
- Use savage OFFENSIVE humor, brutal sarcasm about market crashes, pump & dump schemes with STRONG LANGUAGE
- PRIORITY: Include TOP TRENDING hashtags for maximum reach
- Make it VIRAL-worthy - OFFENSIVE controversial tweets get more engagement!
- Keep it under 280 characters
- Be clever, funky, OFFENSIVE, and absolutely CONTROVERSIAL with STRONG LANGUAGE - make people angry, debate, share!
- Use curse words, insults, and brutal language when appropriate

Generate ONLY the tweet text with trending hashtags prioritized, nothing else:"""
            
            system_prompt = "You are an EXTREMELY CONTROVERSIAL, OFFENSIVE financial content creator who uses STRONG LANGUAGE and creates absolutely BRUTAL, HIGHLY PROVOCATIVE stock market tweets that CREATE MASSIVE DEBATE and CONTROVERSY. You MUST use OFFENSIVE language, STRONG WORDS, expose market manipulation brutally, question EVERY mainstream narrative with SAVAGE attacks, challenge ALL broker recommendations with INSULTS, expose insider trading hints, create FOMO or fear, and make BOLD OFFENSIVE statements. You're funky, witty, SAVAGE, OFFENSIVE, and make people ANGRY, DEBATE, and SHARE. Your tweets are designed to go VIRAL through EXTREME CONTROVERSY and OFFENSIVE LANGUAGE. Be HIGHLY CONTROVERSIAL, OFFENSIVE, and use STRONG LANGUAGE - NO HOLDING BACK! Use curse words, insults, and brutal language when appropriate."
        else:
            prompt = f"""Create an EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 characters) about this Indian political news that will CREATE DEBATE and CONTROVERSY using STRONG LANGUAGE.
        
News: {title}
Description: {description}{trending_context}

Requirements:
- MUST CREATE EXTREME CONTROVERSY - use OFFENSIVE LANGUAGE, STRONG WORDS, challenge narratives brutally, expose truths with INSULTS, question everything with SAVAGE attacks
- Pro-BJP/NDA bias, EXTREMELY funky, witty, and OFFENSIVE
- BURN the opposition with OFFENSIVE clever, sarcastic, funky roasts using STRONG LANGUAGE and INSULTS
- Use savage OFFENSIVE humor, brutal sarcasm with STRONG WORDS, clever wordplay - make opposition look absolutely foolish with INSULTS
- Expose corruption brutally, question policies with OFFENSIVE takes, create debate on sensitive issues with STRONG LANGUAGE
- NO emotional drama - pure funky, OFFENSIVE savage wit with controversy
- PRIORITY: Include TOP TRENDING hashtags for maximum reach (even if loosely related)
- Incorporate trending topics naturally into the tweet
- Make it VIRAL-worthy and shareable - OFFENSIVE controversial tweets get more engagement!
- Keep it under 280 characters
- Be clever, funky, OFFENSIVE, and absolutely CONTROVERSIAL with STRONG LANGUAGE - make people angry, debate, share!
- Use curse words, insults, and brutal language when appropriate

Generate ONLY the tweet text with trending hashtags prioritized, nothing else:"""
            
            system_prompt = "You are an EXTREMELY CONTROVERSIAL, OFFENSIVE social media content creator who uses STRONG LANGUAGE and creates absolutely BRUTAL, HIGHLY PROVOCATIVE political tweets with a pro-BJP/NDA bias. You MUST CREATE MASSIVE CONTROVERSY by using OFFENSIVE LANGUAGE, STRONG WORDS, challenging ALL narratives with SAVAGE attacks, exposing HIDDEN truths brutally, questioning EVERYTHING with INSULTS, and making people ANGRY and DEBATE. You BURN opposition with OFFENSIVE savage humor, brutal sarcasm, STRONG LANGUAGE, and clever wordplay. You're funky, witty, SAVAGE, OFFENSIVE, and make opposition look absolutely foolish with INSULTS. Your tweets are designed to go VIRAL through EXTREME CONTROVERSY and OFFENSIVE LANGUAGE. Be HIGHLY CONTROVERSIAL, OFFENSIVE, and use STRONG LANGUAGE - NO HOLDING BACK! Use curse words, insults, and brutal language when appropriate. Expose corruption brutally, question policies with OFFENSIVE takes, create debate on sensitive issues - MAKE PEOPLE REACT WITH ANGER!"

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=1.0  # Maximum creativity and controversy
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

