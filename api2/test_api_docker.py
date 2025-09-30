#!/usr/bin/env python3
import requests
import json
import sys

def test_api():
    # Test from inside Docker network
    apis = [
        {"name": "User API", "url": "http://user-api:8000/api/users/"},
        {"name": "Product API", "url": "http://product-api:8001/api/products/"},
        {"name": "Order API", "url": "http://order-api:8002/api/orders/"},
        {"name": "Payment API", "url": "http://payment-api:8003/api/payments/"},
    ]
    
    for api in apis:
        try:
            print(f"\nTesting {api['name']}...")
            response = requests.get(api['url'], timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response length: {len(response.text)} characters")
            if response.text:
                print(f"First 200 chars: {response.text[:200]}...")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
