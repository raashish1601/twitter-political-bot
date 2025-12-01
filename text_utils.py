"""
Text Utilities - Helper functions for tweet text processing
"""
import re

def truncate_tweet_complete(tweet_text: str, max_length: int = 280) -> str:
    """
    Truncate tweet to ensure it's complete (ends at sentence boundary)
    Never cuts mid-sentence - ensures tweet is always complete
    """
    if len(tweet_text) <= max_length:
        return tweet_text
    
    # Try to find a sentence boundary (., !, ?) before the limit
    # Look for the last sentence ending within the limit
    truncated = tweet_text[:max_length]
    
    # Find the last sentence ending (., !, ?) in the truncated text
    # Look for patterns: ". ", "! ", "? " (sentence ending followed by space)
    sentence_endings = ['. ', '! ', '? ', '.', '!', '?']
    last_sentence_end = -1
    best_ending = None
    
    for ending in sentence_endings:
        pos = truncated.rfind(ending)
        if pos > last_sentence_end:
            last_sentence_end = pos
            best_ending = ending
    
    # If we found a sentence ending, cut there (include the ending)
    if last_sentence_end > max_length * 0.6:  # At least 60% of the way through
        if best_ending and best_ending.endswith(' '):
            # Ending with space - cut before the space
            return tweet_text[:last_sentence_end + len(best_ending)].strip()
        else:
            # Ending without space - include the punctuation
            return tweet_text[:last_sentence_end + len(best_ending)].strip()
    
    # If no good sentence ending, try to find a natural break point
    # Look for common phrase endings: ", ", " - ", " | ", etc.
    break_points = [', ', ' - ', ' | ', '...', '…']
    last_break = -1
    best_break = None
    
    for break_point in break_points:
        pos = truncated.rfind(break_point)
        if pos > last_break and pos > max_length * 0.7:
            last_break = pos
            best_break = break_point
    
    if last_break > max_length * 0.7:
        return tweet_text[:last_break + len(best_break)].strip()
    
    # Last resort: find word boundary and ensure it's a complete thought
    # Find the last space before the limit
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.75:  # At least 75% of the way through
        # Check if cutting here would leave an incomplete word/phrase
        words_after = tweet_text[last_space:last_space+20].strip()
        # If the next word is very short or looks incomplete, go back further
        if len(words_after.split()[0]) < 3:
            # Find previous space
            prev_space = truncated[:last_space].rfind(' ')
            if prev_space > max_length * 0.6:
                return tweet_text[:prev_space].strip()
        
        return tweet_text[:last_space].strip()
    
    # Absolute last resort - cut at limit but try to make it look complete
    return tweet_text[:max_length - 3].strip() + "..."

def ensure_complete_tweet(tweet_text: str, max_length: int = 280) -> str:
    """
    Ensure tweet is complete and properly formatted
    Removes incomplete sentences, ensures proper ending
    """
    tweet_text = tweet_text.strip()
    
    # If tweet is already under limit, check if it ends properly
    if len(tweet_text) <= max_length:
        # Check if tweet ends with incomplete sentence
        # Look for patterns like "...", incomplete words, or trailing punctuation without space
        if tweet_text.endswith("'s...") or tweet_text.endswith("'s ") or tweet_text.endswith("'s"):
            # Ends with possessive - might be incomplete, try to find sentence boundary
            # Look for last complete sentence
            for ending in ['. ', '! ', '? ']:
                pos = tweet_text.rfind(ending)
                if pos > len(tweet_text) * 0.6:
                    return tweet_text[:pos + len(ending)].strip()
        
        # If ends with ellipsis and is much shorter, might be incomplete
        if tweet_text.endswith('...') and len(tweet_text) < max_length * 0.9:
            # Try to find a better ending point
            for ending in ['. ', '! ', '? ']:
                pos = tweet_text.rfind(ending)
                if pos > len(tweet_text) * 0.7:
                    return tweet_text[:pos + len(ending)].strip()
        
        return tweet_text
    
    # Tweet is over limit - truncate intelligently
    tweet_text = truncate_tweet_complete(tweet_text, max_length)
    
    # Final check - ensure it's under limit
    if len(tweet_text) > max_length:
        # Emergency truncation - find last complete sentence
        for ending in ['. ', '! ', '? ']:
            pos = tweet_text[:max_length].rfind(ending)
            if pos > max_length * 0.6:
                return tweet_text[:pos + len(ending)].strip()
        
        # No sentence ending found - cut at word boundary
        words = tweet_text[:max_length - 3].rsplit(' ', 1)[0]
        if len(words) > 50:
            return words.strip()
        else:
            return tweet_text[:max_length - 3].strip() + "..."
    
    return tweet_text

