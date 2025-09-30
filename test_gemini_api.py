"""
Quick test for Google Gemini API key
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def test_gemini_api():
    """Test Gemini API key with simple request"""
    try:
        api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('GEMINI_API_KEY')
        client = genai.Client(api_key=api_key)

        print("🔑 Testing Gemini API key...")
        print(f"📍 API Key found: {'Yes' if api_key else 'No'}")

        # Test gemini-2.5-flash
        print("\n📊 Testing gemini-2.5-flash...")
        response1 = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="What is 2+2? Answer in one word."
        )
        print(f"Response: {response1.text}")

        print(f"\n✅ API key confirmed working!")
        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_gemini_api()