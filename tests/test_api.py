"""Quick test to verify OpenAI API key"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4o")

print(f"Testing OpenAI API...")
print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
print(f"Model: {model}")
print("-" * 60)

try:
    client = OpenAI(api_key=api_key)
    
    print("\nSending test request...")
    
    # GPT-5 uses max_completion_tokens instead of max_tokens
    params = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'API key is working!' in exactly 5 words."}
        ]
    }
    
    if model.startswith("gpt-5") or model.startswith("o1"):
        params["max_completion_tokens"] = 50
    else:
        params["max_tokens"] = 50
    
    response = client.chat.completions.create(**params)
    
    print("\n✓ SUCCESS!")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Model used: {response.model}")
    print(f"Tokens used: {response.usage.total_tokens}")
    print(f"Cost: ~${(response.usage.total_tokens / 1000000) * 10:.6f}")
    
except Exception as e:
    print("\n✗ FAILED!")
    print(f"Error: {e}")
    print("\nPossible issues:")
    print("1. Invalid or expired API key")
    print("2. Model name incorrect (try 'gpt-4o' instead of 'gpt-5')")
    print("3. No API credits/quota remaining")
    print("4. Network connection issue")
