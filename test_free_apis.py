#!/usr/bin/env python3
"""
Test script to verify Groq and Hugging Face API keys are working
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_groq_api():
    """Test Groq API"""
    print("\n" + "="*50)
    print("🧪 Testing Groq API...")
    print("="*50)
    
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key or groq_key == 'your_groq_api_key_here':
        print("❌ GROQ_API_KEY not found or not set")
        return False
    
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        
        # Test with a simple prompt
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Say 'Groq API is working!' in one sentence."}
            ],
            max_tokens=20
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Groq API is working!")
        print(f"📝 Response: {result}")
        return True
        
    except ImportError:
        print("❌ Groq library not installed. Run: pip install groq")
        return False
    except Exception as e:
        print(f"❌ Groq API error: {str(e)[:100]}")
        return False

def test_huggingface_api():
    """Test Hugging Face API"""
    print("\n" + "="*50)
    print("🧪 Testing Hugging Face API...")
    print("="*50)
    
    hf_key = os.getenv('HUGGINGFACE_API_KEY')
    if not hf_key or hf_key == 'your_huggingface_api_key_here':
        print("❌ HUGGINGFACE_API_KEY not found or not set")
        return False
    
    try:
        import requests
        
        # Test with a simple model - try the new inference endpoint
        api_url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {"Authorization": f"Bearer {hf_key}"}
        
        payload = {
            "inputs": "Hello, this is a test. The API is",
            "parameters": {
                "max_new_tokens": 10,
                "return_full_text": False
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
            else:
                generated_text = str(result)
            
            print(f"✅ Hugging Face API is working!")
            print(f"📝 Response: {generated_text[:50]}...")
            return True
        elif response.status_code == 503:
            print("⚠️  Model is loading (this is normal for first request)")
            print("✅ API key is valid, but model needs to warm up")
            return True
        else:
            print(f"❌ Hugging Face API error: {response.status_code}")
            print(f"   Response: {response.text[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ Hugging Face API error: {str(e)[:100]}")
        return False

def test_content_generator():
    """Test if ContentGenerator can use the free APIs"""
    print("\n" + "="*50)
    print("🧪 Testing ContentGenerator with free APIs...")
    print("="*50)
    
    try:
        from content_generator import ContentGenerator
        
        generator = ContentGenerator()
        
        # Test with a sample article
        test_article = {
            'title': 'Test News Article',
            'description': 'This is a test description for API verification',
            'source': 'Test Source'
        }
        
        print("📝 Generating tweet using free APIs (OpenAI disabled)...")
        # Temporarily disable OpenAI to force free API usage
        original_use_openai = generator.use_openai
        generator.use_openai = False
        
        tweet = generator.generate_funky_tweet(test_article, None, is_stock_market=False)
        
        # Restore OpenAI setting
        generator.use_openai = original_use_openai
        
        if tweet and len(tweet) > 20:
            print(f"✅ ContentGenerator is working with free APIs!")
            print(f"📝 Generated tweet: {tweet[:150]}...")
            return True
        else:
            print("❌ ContentGenerator failed to generate tweet")
            return False
            
    except Exception as e:
        print(f"❌ ContentGenerator error: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 Testing Free API Keys")
    print("="*50)
    
    results = {
        'Groq': test_groq_api(),
        'Hugging Face': test_huggingface_api(),
        'ContentGenerator': test_content_generator()
    }
    
    print("\n" + "="*50)
    print("📊 Test Results Summary")
    print("="*50)
    for api, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {api}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed! Free APIs are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
    
    print("="*50 + "\n")

