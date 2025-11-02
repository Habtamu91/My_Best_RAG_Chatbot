"""Quick test script that uses urllib instead of requests (built-in)."""
import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("=" * 50)
    print("Test 1: Health Check")
    print("=" * 50)
    try:
        req = urllib.request.Request(f"{BASE_URL}/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"✓ Status Code: {response.status}")
            print(f"✓ Response: {json.dumps(data, indent=2)}")
            return data.get("status") == "healthy"
    except urllib.error.URLError as e:
        print(f"✗ Failed: Cannot connect to server: {e}")
        print("  → Start the backend with: python run.py")
        return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_chat_no_documents():
    """Test chat when no documents are uploaded."""
    print("\n" + "=" * 50)
    print("Test 2: Chat with No Documents")
    print("=" * 50)
    try:
        payload = {"question": "What is this document about?"}
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode())
            print(f"✓ Status Code: {response.status}")
            print(f"✓ Response: {json.dumps(result, indent=2)}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 500:
            print(f"⚠ Note: Server error (might be normal if no documents uploaded)")
            return False
        print(f"✗ Failed: HTTP {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("RAG Chatbot - Quick Test Suite (No External Dependencies)")
    print("=" * 50)
    print("\nMake sure the backend is running on http://localhost:8000")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nTest cancelled.")
        sys.exit(0)
    
    results = []
    results.append(("Health Check", test_health()))
    
    # Only test chat if server is accessible
    if results[0][1]:
        results.append(("Chat (No Docs)", test_chat_no_documents()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed >= 1:  # At least health check passed
        print("\n🎉 Backend is running! You can now use the chatbot.")
        print("\nNext steps:")
        print("1. Open frontend/index.html in your browser")
        print("2. Upload a PDF document")
        print("3. Ask questions about the document")
    else:
        print("\n⚠️  Tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("- Make sure the backend is running: python run.py")
        print("- Check if port 8000 is available")

if __name__ == "__main__":
    main()

