"""
Simple API endpoint verification
"""
import requests

BASE_URL = "http://127.0.0.1:8001/api"

print("Testing API Endpoints")
print("="*60)

# Test endpoints
endpoints = [
    "/users/",
    "/subjects/",
    "/exams/",
    "/notifications/",
    "/attempts/",
]

for endpoint in endpoints:
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\nGET {url}")
        response = requests.get(url, timeout=2)
        print(f"Status: {response.status_code}")
        if response.status_code != 404:
            print(f"Response length: {len(response.text)} bytes")
    except Exception as e:
        print(f"Error: {str(e)}")

# Test registration endpoint
print(f"\n\nPOST {BASE_URL}/users/register/")
try:
    test_user = {
        "email": "test@example.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User",
        "mobile_number": "9876543210"
    }
    response = requests.post(f"{BASE_URL}/users/register/", json=test_user, timeout=2)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "="*60)
