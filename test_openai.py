"""
Quick test script to verify OpenAI API key is working
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def test_openai_key():
    """Test if OpenAI API key is valid and working"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Make sure it's set in GitHub Secrets or .env file")
        return False
    
    print(f"✅ Found OpenAI API key: {api_key[:20]}...")
    print("🧪 Testing API connection...")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Make a simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API key is working' if you can read this."}
            ],
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        print(f"✅ OpenAI API is working!")
        print(f"📝 Response: {result}")
        print(f"💰 Tokens used: {response.usage.total_tokens} (Input: {response.usage.prompt_tokens}, Output: {response.usage.completion_tokens})")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ OpenAI API Error: {error_msg}")
        
        if '401' in error_msg or 'authentication' in error_msg.lower() or 'invalid' in error_msg.lower():
            print("   ⚠️  The API key appears to be invalid or expired")
            print("   💡 Check if the key is correct in GitHub Secrets")
        elif '429' in error_msg or 'rate limit' in error_msg.lower():
            print("   ⚠️  Rate limit exceeded - but key is valid!")
        elif 'quota' in error_msg.lower():
            print("   ⚠️  Quota exceeded - add billing to your OpenAI account")
        else:
            print("   ⚠️  Unknown error - check your OpenAI account status")
        
        return False

if __name__ == "__main__":
    print("="*50)
    print("🔍 Testing OpenAI API Key")
    print("="*50)
    print()
    
    success = test_openai_key()
    
    print()
    print("="*50)
    if success:
        print("✅ OpenAI key is working! Bot should be able to generate tweets.")
    else:
        print("❌ OpenAI key test failed. Fix the issue before running the bot.")
    print("="*50)

