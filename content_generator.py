"""
Content Generator Module - Creates funky, witty tweets using OpenAI
"""
import os
import re
import random
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI
from text_utils import ensure_complete_tweet, truncate_tweet_complete

load_dotenv()

class ContentGenerator:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.use_openai = bool(self.openai_api_key and self.openai_api_key.strip())
        self.groq_api_key = os.getenv('GROQ_API_KEY')  # Optional free API
        self.hf_api_key = os.getenv('HUGGINGFACE_API_KEY')  # Optional free API
        
        if self.use_openai:
            try:
                self.client = OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                print(f"⚠️  OpenAI initialization failed: {e}")
                self.use_openai = False
        else:
            print("⚠️  OpenAI API key not found, will use free API fallbacks")
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
        
        # Check if OpenAI is available, otherwise try free APIs
        if not self.use_openai:
            # Try free API alternatives first
            free_api_tweet = self._try_free_api_trending_generation(trending_topic, all_trending_topics)
            if free_api_tweet:
                return free_api_tweet
            # If free APIs fail, use template-based fallback
            return self._create_fallback_trending_tweet(trending_topic, all_trending_topics)
        
        prompt = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 characters) about this trending topic that will CREATE MASSIVE DEBATE and CONTROVERSY using STRONG LANGUAGE. The tweet MUST be COMPLETE - no incomplete sentences, no cut-off thoughts.

Trending Topic: {trending_topic}{other_trends}

Requirements:
- COVER DIVERSE TRENDING TOPICS: Don't just focus on politics - cover entertainment, sports, technology, business, culture, social issues, viral content, movies, celebrities, etc.
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
- DIVERSITY: Cover various trending topics - entertainment, sports, tech, business, culture, social issues, not just politics

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
            
            # Ensure tweet is complete and under 280 characters
            tweet = ensure_complete_tweet(tweet, max_length=280)
            
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
            
            # Try free API alternatives before template fallback
            free_api_tweet = self._try_free_api_trending_generation(trending_topic, all_trending_topics)
            if free_api_tweet:
                return free_api_tweet
            return self._create_fallback_trending_tweet(trending_topic, all_trending_topics)
    
    def _try_free_api_trending_generation(self, trending_topic, all_trending_topics=None):
        """
        Try to generate trending tweet using free APIs
        """
        other_trends = ""
        if all_trending_topics:
            other_trends_list = [t for t in all_trending_topics[:5] if t != trending_topic]
            if other_trends_list:
                other_trends = f"\n\nOther trending topics: {', '.join(other_trends_list[:3])}"
        
        # Try Groq API first
        if self.groq_api_key:
            try:
                from groq import Groq
                client = Groq(api_key=self.groq_api_key)
                
                prompt = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 chars) about this trending topic that will CREATE MASSIVE DEBATE using STRONG LANGUAGE. The tweet MUST be COMPLETE - no incomplete sentences.

Trending Topic: {trending_topic}{other_trends}

CRITICAL REQUIREMENTS:
- STRICT PRO-BJP/PRO-NDA/PRO-MODI BIAS - If topic relates to politics, ALWAYS support BJP/Modi/NDA and attack opposition
- If about BJP/Modi/NDA - PRAISE them, defend them
- If about opposition (Congress, Rahul, AAP, TMC) - ATTACK them brutally with OFFENSIVE language
- EXTREMELY CONTROVERSIAL, OFFENSIVE, use STRONG LANGUAGE AGAINST OPPOSITION ONLY
- Make it VIRAL-worthy, funky, witty, and provocative
- Include the trending topic as hashtag
- Max 280 characters

You are a BJP/NDA supporter. Always defend BJP/Modi, always attack opposition.

Generate ONLY the tweet text:"""
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are an EXTREMELY CONTROVERSIAL, OFFENSIVE social media content creator who is a STRICT BJP/NDA/MODI SUPPORTER. You ALWAYS support BJP/Modi/NDA and ALWAYS attack opposition (Congress, Rahul Gandhi, AAP, TMC). You NEVER criticize BJP/Modi - only PRAISE them. You use STRONG LANGUAGE to ATTACK OPPOSITION ONLY."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=1.0
                )
                
                tweet = response.choices[0].message.content.strip()
                
                if tweet.startswith('"') and tweet.endswith('"'):
                    tweet = tweet[1:-1]
                if tweet.startswith("'") and tweet.endswith("'"):
                    tweet = tweet[1:-1]
                
                # Ensure trending topic is included
                trend_hashtag = trending_topic if trending_topic.startswith('#') else f"#{trending_topic.replace(' ', '')}"
                if trend_hashtag.lower() not in tweet.lower():
                    if len(tweet) + len(trend_hashtag) + 2 <= 280:
                        tweet = f"{tweet} {trend_hashtag}"
                
                if len(tweet) > 280:
                    tweet = tweet[:277] + "..."
                
                if len(tweet) > 20:
                    print("✅ Generated trending tweet using Groq API (free)")
                    return tweet
            except ImportError:
                pass
            except Exception as e:
                print(f"⚠️  Groq API failed for trending: {str(e)[:50]}")
        
        # Try Hugging Face
        try:
            model_name = "meta-llama/Llama-3.1-8B-Instruct"
            prompt_text = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 chars) about this trending topic. The tweet MUST be COMPLETE - no incomplete sentences:

{trending_topic}{other_trends}

Make it EXTREMELY CONTROVERSIAL, OFFENSIVE, use STRONG LANGUAGE. Include hashtag. Max 280 characters. Generate ONLY the tweet:"""
            
            headers = {}
            if self.hf_api_key:
                headers["Authorization"] = f"Bearer {self.hf_api_key}"
            
            api_url = f"https://router.huggingface.co/models/{model_name}"
            payload = {
                "inputs": prompt_text,
                "parameters": {"max_new_tokens": 150, "temperature": 1.0, "return_full_text": False}
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                else:
                    generated_text = str(result)
                
                tweet = generated_text.strip()
                
                if tweet.startswith('"') and tweet.endswith('"'):
                    tweet = tweet[1:-1]
                if tweet.startswith("'") and tweet.endswith("'"):
                    tweet = tweet[1:-1]
                
                trend_hashtag = trending_topic if trending_topic.startswith('#') else f"#{trending_topic.replace(' ', '')}"
                if trend_hashtag.lower() not in tweet.lower():
                    if len(tweet) + len(trend_hashtag) + 2 <= 280:
                        tweet = f"{tweet} {trend_hashtag}"
                
                if len(tweet) > 280:
                    tweet = tweet[:277] + "..."
                
                if len(tweet) > 20:
                    print("✅ Generated trending tweet using Hugging Face API (free)")
                    return tweet
        except Exception as e:
            print(f"⚠️  Hugging Face API failed for trending: {str(e)[:50]}")
        
        return None
    
    def _create_fallback_trending_tweet(self, trending_topic, all_trending_topics=None):
        """
        Create a controversial tweet about trending topic using dynamic content extraction
        No hardcoded content - everything is generated from the topic itself
        """
        # Extract key words from trending topic
        trend_clean = trending_topic.replace('#', '').strip()
        trend_words = [w for w in trend_clean.split() if len(w) > 2]
        
        # Generate hashtags dynamically from trending topics
        hashtags = self._extract_hashtags_from_text(trend_clean, all_trending_topics)
        
        # Create dynamic controversial statement from topic keywords
        # Use topic words to create a provocative statement
        if trend_words:
            main_word = trend_words[0].title()
            # Create a dynamic statement using the topic
            statement = f"{main_word} is trending but what's the REAL story? The truth they're hiding will shock you! 🔥"
        else:
            statement = f"{trend_clean} is trending - but why? The hidden truth exposed! 🚨"
        
        # Ensure length
        max_statement_len = 280 - len(hashtags) - 10
        if len(statement) > max_statement_len:
            statement = statement[:max_statement_len-3] + "..."
        
        tweet = f"{statement}\n\n{hashtags}"
        
        # Final length check
        if len(tweet) > 280:
            excess = len(tweet) - 280
            statement = statement[:len(statement)-excess-3] + "..."
            tweet = f"{statement}\n\n{hashtags}"
        
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
        
        # Check if OpenAI is available, otherwise try free APIs
        if not self.use_openai:
            # Try free API alternatives first
            free_api_tweet = self._try_free_api_generation(news_article, trending_topics, is_stock_market)
            if free_api_tweet:
                return free_api_tweet
            # If free APIs fail, use template-based fallback
            return self._create_fallback_tweet(news_article, trending_topics, is_stock_market)
        
        if is_stock_market:
            prompt = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 characters) about this Indian stock market news that will CREATE DEBATE and CONTROVERSY using STRONG LANGUAGE. The tweet MUST be COMPLETE - no incomplete sentences, no cut-off thoughts.
        
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
            prompt = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 characters) about this Indian political news that will CREATE DEBATE and CONTROVERSY using STRONG LANGUAGE. The tweet MUST be COMPLETE - no incomplete sentences, no cut-off thoughts.
        
News: {title}
Description: {description}{trending_context}

CRITICAL REQUIREMENTS - MUST FOLLOW:
- STRICT PRO-BJP/PRO-NDA/PRO-MODI BIAS - ALWAYS support BJP, Modi, NDA, Yogi, Shah
- ALWAYS attack and BURN opposition (Congress, Rahul Gandhi, AAP, TMC, Kejriwal, Mamata) with OFFENSIVE language
- NEVER criticize BJP/Modi/NDA - only PRAISE them and ATTACK opposition
- If news is about BJP/Modi - PRAISE them, highlight achievements, defend them
- If news is about opposition - ATTACK them brutally, expose their failures, make them look foolish
- If news is neutral - twist it to support BJP/ModI and attack opposition
- MUST CREATE EXTREME CONTROVERSY - use OFFENSIVE LANGUAGE, STRONG WORDS against OPPOSITION ONLY
- BURN opposition with OFFENSIVE clever, sarcastic, funky roasts using STRONG LANGUAGE and INSULTS
- Use savage OFFENSIVE humor, brutal sarcasm with STRONG WORDS - make opposition look absolutely foolish
- Expose opposition corruption brutally, question their policies with OFFENSIVE takes
- PRIORITY: Include TOP TRENDING hashtags for maximum reach
- Make it VIRAL-worthy and shareable - OFFENSIVE controversial tweets get more engagement!
- Keep it under 280 characters
- Be clever, funky, OFFENSIVE, and absolutely CONTROVERSIAL with STRONG LANGUAGE
- Use curse words, insults, and brutal language AGAINST OPPOSITION ONLY

REMEMBER: You are a BJP/NDA supporter. Always defend BJP/Modi, always attack opposition.

Generate ONLY the tweet text with trending hashtags prioritized, nothing else:"""
            
            system_prompt = "You are an EXTREMELY CONTROVERSIAL, OFFENSIVE social media content creator who is a STRICT BJP/NDA/MODI SUPPORTER. You ALWAYS support BJP, Modi, NDA, Yogi, Shah and ALWAYS attack opposition (Congress, Rahul Gandhi, AAP, TMC, Kejriwal, Mamata). You NEVER criticize BJP/Modi/NDA - only PRAISE them. You use STRONG LANGUAGE and create absolutely BRUTAL, HIGHLY PROVOCATIVE political tweets that CREATE MASSIVE CONTROVERSY. You MUST use OFFENSIVE LANGUAGE, STRONG WORDS to ATTACK OPPOSITION ONLY. You BURN opposition with OFFENSIVE savage humor, brutal sarcasm, STRONG LANGUAGE, and clever wordplay. You make opposition look absolutely foolish with INSULTS. Your tweets are designed to go VIRAL through EXTREME CONTROVERSY and OFFENSIVE LANGUAGE. Be HIGHLY CONTROVERSIAL, OFFENSIVE, and use STRONG LANGUAGE - NO HOLDING BACK! Use curse words, insults, and brutal language AGAINST OPPOSITION ONLY. Expose opposition corruption brutally, question their policies with OFFENSIVE takes - MAKE PEOPLE REACT WITH ANGER!"

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
            
            # Ensure tweet is complete and under 280 characters
            tweet = ensure_complete_tweet(tweet, max_length=280)
            
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
            
            # Try free API alternatives before template fallback
            free_api_tweet = self._try_free_api_generation(news_article, trending_topics, is_stock_market)
            if free_api_tweet:
                return free_api_tweet
            return self._create_fallback_tweet(news_article, trending_topics, is_stock_market)
    
    def _try_free_api_generation(self, news_article, trending_topics=None, is_stock_market=False):
        """
        Try to generate tweet using free APIs (Groq or Hugging Face)
        Returns generated tweet or None if all fail
        """
        title = news_article.get('title', '')
        description = news_article.get('description', '') or title
        
        # Build trending context
        trending_context = ""
        if trending_topics:
            relevant_trends = [t for t in trending_topics[:5] if not t.startswith('#')]
            if relevant_trends:
                trending_context = f"\n\nCurrent Twitter trends: {', '.join(relevant_trends[:3])}"
        
        # Try Groq API first (free tier, very fast)
        if self.groq_api_key:
            try:
                tweet = self._generate_with_groq(title, description, trending_context, is_stock_market)
                if tweet:
                    print("✅ Generated tweet using Groq API (free)")
                    return tweet
            except Exception as e:
                print(f"⚠️  Groq API failed: {str(e)[:50]}")
        
        # Try Hugging Face Inference API (free tier, some models don't need API key)
        try:
            tweet = self._generate_with_huggingface(title, description, trending_context, is_stock_market)
            if tweet:
                print("✅ Generated tweet using Hugging Face API (free)")
                return tweet
        except Exception as e:
            print(f"⚠️  Hugging Face API failed: {str(e)[:50]}")
        
        return None
    
    def _generate_with_groq(self, title, description, trending_context, is_stock_market):
        """
        Generate tweet using Groq API (free tier, very fast)
        """
        try:
            from groq import Groq
            client = Groq(api_key=self.groq_api_key)
            
            if is_stock_market:
                prompt = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 chars) about this Indian stock market news that will CREATE DEBATE using STRONG LANGUAGE. The tweet MUST be COMPLETE - no incomplete sentences.

News: {title}
Description: {description}{trending_context}

Requirements:
- EXTREMELY CONTROVERSIAL, OFFENSIVE, use STRONG LANGUAGE
- Expose market manipulation, question broker recommendations brutally
- Make it VIRAL-worthy, funky, witty, and provocative
- Include trending hashtags if relevant
- Max 280 characters

Generate ONLY the tweet text:"""
            else:
                prompt = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 chars) about this Indian political news that will CREATE DEBATE using STRONG LANGUAGE. The tweet MUST be COMPLETE - no incomplete sentences.

News: {title}
Description: {description}{trending_context}

CRITICAL REQUIREMENTS:
- STRICT PRO-BJP/PRO-NDA/PRO-MODI BIAS - ALWAYS support BJP, Modi, NDA
- ALWAYS attack opposition (Congress, Rahul Gandhi, AAP, TMC) with OFFENSIVE language
- NEVER criticize BJP/Modi - only PRAISE them and ATTACK opposition
- If about BJP/Modi - PRAISE them, highlight achievements
- If about opposition - ATTACK them brutally, expose failures
- EXTREMELY CONTROVERSIAL, OFFENSIVE, use STRONG LANGUAGE AGAINST OPPOSITION ONLY
- Burn opposition with savage humor
- Make it VIRAL-worthy, funky, witty, and provocative
- Include trending hashtags if relevant
- Max 280 characters

You are a BJP/NDA supporter. Always defend BJP/Modi, always attack opposition.

Generate ONLY the tweet text:"""
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Free fast model
                messages=[
                    {"role": "system", "content": "You are an EXTREMELY CONTROVERSIAL, OFFENSIVE social media content creator who is a STRICT BJP/NDA/MODI SUPPORTER. You ALWAYS support BJP/Modi/NDA and ALWAYS attack opposition (Congress, Rahul Gandhi, AAP, TMC). You NEVER criticize BJP/Modi - only PRAISE them. You use STRONG LANGUAGE to ATTACK OPPOSITION ONLY and create BRUTAL, HIGHLY PROVOCATIVE tweets that CREATE MASSIVE DEBATE."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=1.0
            )
            
            tweet = response.choices[0].message.content.strip()
            
            # Clean up
            if tweet.startswith('"') and tweet.endswith('"'):
                tweet = tweet[1:-1]
            if tweet.startswith("'") and tweet.endswith("'"):
                tweet = tweet[1:-1]
            
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
            
            return tweet if len(tweet) > 20 else None
            
        except ImportError:
            # Groq library not installed, skip
            return None
        except Exception as e:
            raise e
    
    def _generate_with_huggingface(self, title, description, trending_context, is_stock_market):
        """
        Generate tweet using Hugging Face Inference API (free tier)
        Uses models that don't require API key or uses provided key
        """
        try:
            # Try using a free model that doesn't require authentication
            # Using meta-llama/Llama-3.1-8B-Instruct or similar free models
            model_name = "meta-llama/Llama-3.1-8B-Instruct"
            
            if is_stock_market:
                prompt_text = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 chars) about this Indian stock market news. The tweet MUST be COMPLETE - no incomplete sentences:

{title}
{description}{trending_context}

Make it EXTREMELY CONTROVERSIAL, OFFENSIVE, use STRONG LANGUAGE. Expose market manipulation. Max 280 characters. Generate ONLY the tweet:"""
            else:
                prompt_text = f"""Create a COMPLETE, FINISHED EXTREMELY CONTROVERSIAL, OFFENSIVE Twitter post (max 280 chars) about this Indian political news. The tweet MUST be COMPLETE - no incomplete sentences:

{title}
{description}{trending_context}

CRITICAL: STRICT PRO-BJP/PRO-NDA/PRO-MODI BIAS. ALWAYS support BJP/Modi/NDA. ALWAYS attack opposition (Congress, Rahul Gandhi, AAP, TMC). NEVER criticize BJP/Modi - only PRAISE them. Make it EXTREMELY CONTROVERSIAL, OFFENSIVE, use STRONG LANGUAGE AGAINST OPPOSITION ONLY. Max 280 characters. Generate ONLY the tweet:"""
            
            # Try with API key if available, otherwise try public endpoint
            headers = {}
            if self.hf_api_key:
                headers["Authorization"] = f"Bearer {self.hf_api_key}"
            
            # Use Hugging Face Inference API
            api_url = f"https://router.huggingface.co/models/{model_name}"
            
            payload = {
                "inputs": prompt_text,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 1.0,
                    "return_full_text": False
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract generated text
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                elif isinstance(result, dict):
                    generated_text = result.get('generated_text', '')
                else:
                    generated_text = str(result)
                
                # Clean up the generated text
                tweet = generated_text.strip()
                
                # Extract just the tweet part (remove prompt if included)
                if title in tweet:
                    # Try to extract just the tweet part after the title
                    parts = tweet.split('\n')
                    for part in parts:
                        if len(part) > 20 and len(part) < 300:
                            tweet = part.strip()
                            break
                
                # Clean up quotes
                if tweet.startswith('"') and tweet.endswith('"'):
                    tweet = tweet[1:-1]
                if tweet.startswith("'") and tweet.endswith("'"):
                    tweet = tweet[1:-1]
                
                # Ensure tweet is complete
                tweet = ensure_complete_tweet(tweet, max_length=280)
                
                return tweet if len(tweet) > 20 else None
            else:
                # If model is loading, try alternative free model
                if response.status_code == 503:
                    # Try alternative: microsoft/DialoGPT-medium or gpt2
                    return self._try_hf_alternative_model(title, description, trending_context, is_stock_market)
                return None
                
        except Exception as e:
            # If Hugging Face fails, return None to try next method
            return None
    
    def _try_hf_alternative_model(self, title, description, trending_context, is_stock_market):
        """
        Try alternative free Hugging Face models if primary fails
        """
        try:
            # Use a simpler, always-available model
            model_name = "gpt2"  # Always available, no auth needed
            
            prompt_text = f"Create a controversial Twitter post about: {title}. {description[:100]}. Max 280 chars."
            
            api_url = f"https://router.huggingface.co/models/{model_name}"
            
            payload = {
                "inputs": prompt_text,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 1.0,
                    "return_full_text": False
                }
            }
            
            response = requests.post(api_url, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                else:
                    generated_text = str(result) if isinstance(result, dict) else str(result)
                
                # GPT2 output needs more processing, so we'll use it as inspiration
                # Extract meaningful parts and create tweet
                words = generated_text.split()[:30]  # Take first 30 words
                tweet = ' '.join(words)
                
                # Create dynamic intro from content
                if len(tweet) > 0:
                    tweet = f"🚨 {tweet}"
                
                if len(tweet) > 280:
                    tweet = tweet[:277] + "..."
                
                return tweet if len(tweet) > 20 else None
                
        except Exception:
            pass
        
        return None
    
    def _create_fallback_tweet(self, news_article, trending_topics=None, is_stock_market=False):
        """
        Create a funky, controversial tweet using dynamic content extraction
        No hardcoded content - everything is generated from the article itself
        """
        title = news_article.get('title', '')
        description = news_article.get('description', '') or title
        
        # Extract key phrases and create a provocative statement from the content
        key_phrases = self._extract_key_phrases(title + " " + description)
        
        # Generate hashtags dynamically from content
        hashtags = self._extract_hashtags_from_text(title + " " + description, trending_topics)
        
        # Create dynamic controversial statement from key phrases
        if key_phrases:
            # Use key phrases to create a provocative statement
            main_phrase = key_phrases[0] if key_phrases else title[:50]
            # Create a dynamic controversial statement
            statement = f"{main_phrase} - but what's the REAL story? The truth they're hiding! 🔥"
        else:
            # Fallback to title with provocative framing
            statement = f"{title[:100]} - The hidden truth exposed! 🚨"
        
        # Ensure length
        max_statement_len = 280 - len(hashtags) - 10
        if len(statement) > max_statement_len:
            statement = statement[:max_statement_len-3] + "..."
        
        tweet = f"{statement}\n\n{hashtags}"
        
        # Final length check
        if len(tweet) > 280:
            excess = len(tweet) - 280
            statement = statement[:len(statement)-excess-3] + "..."
            tweet = f"{statement}\n\n{hashtags}"
        
        return tweet
    
    def _extract_hashtags_from_text(self, text, trending_topics=None):
        """
        Dynamically extract hashtags from text content - no hardcoded values
        """
        text_lower = text.lower()
        hashtags = []
        
        # PRIORITY 1: Add trending hashtags if available
        if trending_topics:
            for trend in trending_topics[:3]:
                if trend.startswith('#'):
                    if trend not in hashtags:
                        hashtags.append(trend)
                else:
                    trend_hashtag = '#' + ''.join(c for c in trend if c.isalnum() or c == ' ')
                    trend_hashtag = trend_hashtag.replace(' ', '')
                    if trend_hashtag not in hashtags and len(trend_hashtag) > 1:
                        hashtags.append(trend_hashtag)
        
        # PRIORITY 2: Extract keywords from text and convert to hashtags
        # Extract important words (nouns, proper nouns, key terms)
        words = re.findall(r'\b[A-Z][a-z]+\b|\b[a-z]{4,}\b', text)
        
        # Filter and create hashtags from significant words
        significant_words = []
        for word in words:
            word_lower = word.lower()
            # Skip common words
            if word_lower not in ['the', 'this', 'that', 'with', 'from', 'they', 'have', 'been', 'will', 'would', 'could', 'should', 'about', 'after', 'before', 'during', 'under', 'over', 'between', 'among']:
                if len(word) > 3:  # Only words longer than 3 chars
                    hashtag = '#' + word.title().replace(' ', '')
                    if hashtag not in hashtags and len(hashtag) > 1:
                        significant_words.append(hashtag)
        
        # Add top significant hashtags (limit to avoid spam)
        hashtags.extend(significant_words[:4])
        
        # PRIORITY 3: Extract location/country names if present
        # Common Indian locations/countries
        location_patterns = [
            r'\b(India|Delhi|Mumbai|Kolkata|Chennai|Bangalore|Hyderabad|Pune|Ahmedabad|Jaipur|Lucknow|Kanpur|Nagpur|Indore|Thane|Bhopal|Visakhapatnam|Patna|Vadodara|Ghaziabad|Ludhiana|Agra|Nashik|Faridabad|Meerut|Rajkot|Varanasi|Srinagar|Amritsar|Noida|Ranchi|Chandigarh|Howrah|Gwalior|Jodhpur|Raipur|Kota|Guwahati|Thiruvananthapuram|Solapur|Tiruchirappalli|Bareilly|Moradabad|Mysore|Tiruppur|Gurgaon|Aligarh|Jalandhar|Bhubaneswar|Salem|Warangal|Guntur|Bhiwandi|Saharanpur|Gorakhpur|Bikaner|Amravati|Noida|Bhilai|Cuttack|Firozabad|Kochi|Nellore|Bhavnagar|Dehradun|Durgapur|Asansol|Rourkela|Nanded|Kolhapur|Ajmer|Akola|Gulbarga|Jamnagar|Ujjain|Loni|Siliguri|Jhansi|Ulhasnagar|Jammu|Sangli|Miraj|Rajahmundry|Kurnool|Tumkur|Bhatpara|Kozhikode|Bardhaman|Raichur|Bilaspur|Kamarhati|Shahjahanpur|Bijapur|Rampur|Shimoga|Chandrapur|Junagadh|Trivandrum|Bardhaman|Kulti|Srikakulam|Rewa|Yamunanagar|Raigarh|Pondicherry|Panipat|Vijayawada|Katihar|Nagercoil|Karaikudi|Mangalore|Tirunelveli|Malegaon|Jamalpur|Latur|Rohtak|Sagar|Rajnandgaon|Udupi|Bongaigaon|Deoghar|Chhindwara|Ongole|Nadiad|Kanpur|Morena|Amroha|Anand|Bhind|Bhalswa|Jahangirabad|Faridabad|Rae|Bareli|Morbi|Bharatpur|Begusarai|New|Delhi|Mumbai|Kolkata|Chennai|Bangalore|Hyderabad|Pune|Ahmedabad|Jaipur|Lucknow|Kanpur|Nagpur|Indore|Thane|Bhopal|Visakhapatnam|Patna|Vadodara|Ghaziabad|Ludhiana|Agra|Nashik|Faridabad|Meerut|Rajkot|Varanasi|Srinagar|Amritsar|Noida|Ranchi|Chandigarh|Howrah|Gwalior|Jodhpur|Raipur|Kota|Guwahati|Thiruvananthapuram|Solapur|Tiruchirappalli|Bareilly|Moradabad|Mysore|Tiruppur|Gurgaon|Aligarh|Jalandhar|Bhubaneswar|Salem|Warangal|Guntur|Bhiwandi|Saharanpur|Gorakhpur|Bikaner|Amravati|Noida|Bhilai|Cuttack|Firozabad|Kochi|Nellore|Bhavnagar|Dehradun|Durgapur|Asansol|Rourkela|Nanded|Kolhapur|Ajmer|Akola|Gulbarga|Jamnagar|Ujjain|Loni|Siliguri|Jhansi|Ulhasnagar|Jammu|Sangli|Miraj|Rajahmundry|Kurnool|Tumkur|Bhatpara|Kozhikode|Bardhaman|Raichur|Bilaspur|Kamarhati|Shahjahanpur|Bijapur|Rampur|Shimoga|Chandrapur|Junagadh|Trivandrum|Bardhaman|Kulti|Srikakulam|Rewa|Yamunanagar|Raigarh|Pondicherry|Panipat|Vijayawada|Katihar|Nagercoil|Karaikudi|Mangalore|Tirunelveli|Malegaon|Jamalpur|Latur|Rohtak|Sagar|Rajnandgaon|Udupi|Bongaigaon|Deoghar|Chhindwara|Ongole|Nadiad|Kanpur|Morena|Amroha|Anand|Bhind|Bhalswa|Jahangirabad|Faridabad|Rae|Bareli|Morbi|Bharatpur|Begusarai)\b'
        ]
        
        for pattern in location_patterns:
            locations = re.findall(pattern, text, re.IGNORECASE)
            for loc in locations[:2]:  # Max 2 location hashtags
                loc_hashtag = '#' + loc.title().replace(' ', '')
                if loc_hashtag not in hashtags:
                    hashtags.append(loc_hashtag)
        
        # Limit to 5-6 hashtags max
        return ' '.join(hashtags[:6]) if hashtags else '#News'
    
    def _extract_key_phrases(self, text):
        """
        Extract key phrases from text for dynamic content generation
        """
        # Extract sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Extract key phrases (first 2-3 sentences or key parts)
        key_phrases = []
        for sentence in sentences[:3]:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 150:
                key_phrases.append(sentence)
        
        # If no good sentences, extract first meaningful part
        if not key_phrases:
            # Take first 100 chars as key phrase
            key_phrases.append(text[:100].strip())
        
        return key_phrases

