#!/usr/bin/env python3
"""
Test script to verify POST requests work with the product API
"""
import requests
import json
import time

def test_product_api():
    base_url = "http://localhost:8001"
    
    print("Testing Product API POST endpoint...")
    
    # Test data
    test_product = {
        "name": "Test Product",
        "price": "29.99",
        "description": "A test product for API testing",
        "stock_quantity": 100,
        "mode": "active"
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        # Test POST request
        print(f"Making POST request to {base_url}/")
        response = requests.post(
            f"{base_url}/",
            json=test_product,
            headers=headers,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 201:
            print("POST request successful!")
            return True
        else:
            print(f"POST request failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False

def test_get_products():
    base_url = "http://localhost:8001"
    
    print("\nTesting GET products endpoint...")
    
    try:
        response = requests.get(f"{base_url}/", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            print("GET request successful!")
            return True
        else:
            print(f"GET request failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False

def test_metrics():
    base_url = "http://localhost:8001"
    
    print("\nTesting metrics endpoint...")
    
    try:
        response = requests.get(f"{base_url}/metrics", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Content (first 500 chars): {response.text[:500]}")
        
        if response.status_code == 200:
            print("Metrics endpoint successful!")
            return True
        else:
            print(f"Metrics endpoint failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Product API Test Suite")
    print("=" * 50)
    
    # Test all endpoints
    post_success = test_product_api()
    get_success = test_get_products()
    metrics_success = test_metrics()
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print(f"POST /: {'PASS' if post_success else 'FAIL'}")
    print(f"GET /: {'PASS' if get_success else 'FAIL'}")
    print(f"GET /metrics: {'PASS' if metrics_success else 'FAIL'}")
    print("=" * 50)
