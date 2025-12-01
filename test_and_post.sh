#!/bin/bash
# Test OpenAI key and then run the bot to post a test tweet

echo "=========================================="
echo "🧪 Testing OpenAI Key First..."
echo "=========================================="
echo ""

# Test OpenAI key
python test_openai.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ OpenAI key works! Now testing full bot..."
    echo "=========================================="
    echo ""
    
    # Run the bot with force flag to ensure it posts
    python main.py --test --force
else
    echo ""
    echo "=========================================="
    echo "❌ OpenAI key test failed. Not running bot."
    echo "=========================================="
    exit 1
fi

