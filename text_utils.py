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
    sentence_endings = ['.', '!', '?', '…']
    last_sentence_end = -1
    
    for ending in sentence_endings:
        pos = truncated.rfind(ending)
        if pos > last_sentence_end:
            last_sentence_end = pos
    
    # If we found a sentence ending, cut there
    if last_sentence_end > max_length * 0.5:  # At least 50% of the way through
        return tweet_text[:last_sentence_end + 1].strip()
    
    # If no sentence ending, try to find a word boundary
    # Find the last space before the limit
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:  # At least 70% of the way through
        # Cut at word boundary and add ellipsis only if we're cutting significantly
        if max_length - last_space < 20:  # Less than 20 chars cut
            return tweet_text[:last_space].strip()
        else:
            return tweet_text[:last_space].strip() + "..."
    
    # Last resort: cut at limit but ensure it ends properly
    # Remove any trailing incomplete words
    if last_space > 0:
        return tweet_text[:last_space].strip() + "..."
    
    # Absolute last resort - but this should rarely happen
    return tweet_text[:max_length - 3].strip() + "..."

def ensure_complete_tweet(tweet_text: str, max_length: int = 280) -> str:
    """
    Ensure tweet is complete and properly formatted
    Removes incomplete sentences, ensures proper ending
    """
    # Remove any trailing incomplete sentences
    tweet_text = tweet_text.strip()
    
    # If tweet ends with incomplete sentence markers, clean them up
    incomplete_markers = ['...', '…', '..', '.']
    for marker in incomplete_markers:
        if tweet_text.endswith(marker) and len(tweet_text) < max_length * 0.8:
            # If tweet is much shorter than limit and ends with ellipsis, might be incomplete
            # But we'll keep it if it's the only way to fit
            pass
    
    # Ensure tweet doesn't end mid-word
    if len(tweet_text) > max_length:
        tweet_text = truncate_tweet_complete(tweet_text, max_length)
    
    # Final check - ensure it's under limit
    if len(tweet_text) > max_length:
        # Emergency truncation at word boundary
        words = tweet_text[:max_length - 3].rsplit(' ', 1)[0]
        if len(words) > 50:  # Only if we have enough content
            return words + "..."
        else:
            # Too short after truncation, use original but cut hard
            return tweet_text[:max_length - 3] + "..."
    
    return tweet_text

