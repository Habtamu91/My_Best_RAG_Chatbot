"""Test script to verify Gemini API setup."""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=" * 50)
print("Testing Gemini API Setup")
print("=" * 50)
print()

# Test 1: Check .env file
print("Test 1: Checking .env file...")
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    print("OK: .env file exists")
    with open(env_path) as f:
        content = f.read()
        if "GEMINI_API_KEY" in content:
            # Extract key (without exposing full key)
            for line in content.split("\n"):
                if line.startswith("GEMINI_API_KEY"):
                    key = line.split("=")[1].strip()
                    print(f"OK: GEMINI_API_KEY found (length: {len(key)} chars)")
                    print(f"  Key starts with: {key[:20]}...")
                    break
        else:
            print("ERROR: GEMINI_API_KEY not found in .env")
            sys.exit(1)
else:
    print("ERROR: .env file not found")
    sys.exit(1)

print()

# Test 2: Check google-generativeai installation
print("Test 2: Checking google-generativeai package...")
try:
    import google.generativeai as genai
    print("OK: google-generativeai is installed")
except ImportError:
    print("ERROR: google-generativeai not installed")
    print("  Install with: pip install google-generativeai")
    sys.exit(1)

print()

# Test 3: Test configuration loading
print("Test 3: Testing configuration...")
try:
    from app.utils.config import GEMINI_API_KEY, LLM_PROVIDER, USE_GEMINI
    print(f"OK: Configuration loaded successfully")
    print(f"  GEMINI_API_KEY: {'OK Set' if GEMINI_API_KEY else 'ERROR Not set'}")
    print(f"  LLM_PROVIDER: {LLM_PROVIDER}")
    print(f"  USE_GEMINI: {USE_GEMINI}")
    if not GEMINI_API_KEY:
        print("  ⚠️  WARNING: GEMINI_API_KEY is empty")
        sys.exit(1)
except Exception as e:
    print(f"ERROR: Error loading configuration: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Test Gemini API connection
print("Test 4: Testing Gemini API connection...")
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Try newer model first, fallback to older if needed
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        try:
            model = genai.GenerativeModel('gemini-pro')
        except:
            model = genai.GenerativeModel('models/gemini-pro')
    response = model.generate_content("Say hello in one word")
    print("OK: Gemini API connection successful!")
    print(f"  Test response: {response.text.strip()}")
except Exception as e:
    print(f"ERROR: Gemini API connection failed: {e}")
    print("  Check your API key is valid")
    sys.exit(1)

print()
print("=" * 50)
print("SUCCESS: All tests passed! Gemini is configured correctly!")
print("=" * 50)
print()
print("Next steps:")
print("1. Restart the backend server")
print("2. Upload a PDF in the frontend")
print("3. Ask questions - you should get Gemini responses!")

