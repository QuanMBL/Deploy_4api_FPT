#!/usr/bin/env python3
"""
Simple test to check if the API is accessible
"""
import requests
import time

def test_connection():
    url = "http://localhost:8001/"
    
    print(f"Testing connection to {url}")
    
    try:
        # Test with a very short timeout
        response = requests.get(url, timeout=2)
        print(f"Success! Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return True
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return False
    except Exception as e:
        print(f"Other error: {e}")
        return False

if __name__ == "__main__":
    print("Simple API Connection Test")
    print("=" * 30)
    
    # Test multiple times
    for i in range(3):
        print(f"\nAttempt {i+1}:")
        success = test_connection()
        if success:
            break
        time.sleep(2)
    
    if not success:
        print("\nAll attempts failed. The API might not be running properly.")
