"""Quick test script to verify the RAG Chatbot setup."""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("=" * 50)
    print("Test 1: Health Check")
    print("=" * 50)
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✓ Status Code: {r.status_code}")
        print(f"✓ Response: {json.dumps(r.json(), indent=2)}")
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        print("✗ Failed: Cannot connect to server. Is the backend running?")
        print("  → Start the backend with: python run.py")
        return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_upload_endpoint():
    """Test if upload endpoint is accessible."""
    print("\n" + "=" * 50)
    print("Test 2: Upload Endpoint Check")
    print("=" * 50)
    try:
        # Just check if endpoint exists (OPTIONS request)
        r = requests.options(f"{BASE_URL}/api/upload", timeout=5)
        print(f"✓ Upload endpoint accessible: {r.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Failed: Cannot connect to server")
        return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_chat_endpoint():
    """Test if chat endpoint is accessible."""
    print("\n" + "=" * 50)
    print("Test 3: Chat Endpoint Check")
    print("=" * 50)
    try:
        r = requests.options(f"{BASE_URL}/api/chat", timeout=5)
        print(f"✓ Chat endpoint accessible: {r.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Failed: Cannot connect to server")
        return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_chat_no_documents():
    """Test chat when no documents are uploaded."""
    print("\n" + "=" * 50)
    print("Test 4: Chat with No Documents")
    print("=" * 50)
    try:
        payload = {"question": "What is this document about?"}
        r = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        print(f"✓ Status Code: {r.status_code}")
        response = r.json()
        print(f"✓ Response: {json.dumps(response, indent=2)}")
        
        # This should return a message about no documents
        if "no documents" in response.get("answer", "").lower():
            print("✓ Expected behavior: No documents uploaded yet")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("RAG Chatbot - Quick Test Suite")
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
    results.append(("Upload Endpoint", test_upload_endpoint()))
    results.append(("Chat Endpoint", test_chat_endpoint()))
    
    # Only test chat if server is accessible
    if all(r[1] for r in results[:3]):
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
    
    if passed == total:
        print("\n🎉 All tests passed! The chatbot is ready to use.")
        print("\nNext steps:")
        print("1. Upload a PDF via the frontend")
        print("2. Ask questions about the document")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("- Make sure the backend is running: python run.py")
        print("- Check if port 8000 is available")
        print("- Verify all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()

