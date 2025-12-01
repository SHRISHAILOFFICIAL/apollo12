"""
Test the complete authentication flow
Run: python test_auth_flow.py
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_signup():
    """Test user signup"""
    print_section("TEST 1: User Signup")
    
    signup_data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "name": "Test User",
        "mobile": "1234567890",
        "password": "password123",
        "confirm_password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup/", json=signup_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Signup successful!")
        return response.json()
    else:
        print("❌ Signup failed!")
        return None

def test_signup_validation():
    """Test signup validation errors"""
    print_section("TEST 2: Signup Validation (Password Mismatch)")
    
    signup_data = {
        "username": "testuser456",
        "email": "testuser456@example.com",
        "name": "Test User 2",
        "mobile": "9876543210",
        "password": "password123",
        "confirm_password": "different123"  # Intentional mismatch
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup/", json=signup_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✅ Validation working correctly!")
    else:
        print("❌ Validation failed!")

def test_login(username, password):
    """Test user login"""
    print_section(f"TEST 3: User Login ({username})")
    
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        return response.json()
    else:
        print("❌ Login failed!")
        return None

def test_login_invalid():
    """Test login with invalid credentials"""
    print_section("TEST 4: Login with Invalid Credentials")
    
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401 and "Invalid username or password" in response.json().get("error", ""):
        print("✅ Error handling working correctly!")
    else:
        print("❌ Error handling failed!")

def test_me_endpoint(access_token):
    """Test /auth/me/ endpoint"""
    print_section("TEST 5: Get Current User (/auth/me/)")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me/", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ /auth/me/ working correctly!")
    else:
        print("❌ /auth/me/ failed!")

def main():
    print("\n" + "="*60)
    print("  AUTHENTICATION FLOW TEST SUITE")
    print("="*60)
    print("\nMake sure the backend server is running on http://localhost:8000\n")
    
    try:
        # Test 1: Signup
        signup_result = test_signup()
        
        # Test 2: Signup validation
        test_signup_validation()
        
        # Test 3: Login with created user
        if signup_result:
            login_result = test_login("testuser123", "password123")
            
            # Test 4: Invalid login
            test_login_invalid()
            
            # Test 5: /auth/me/ endpoint
            if login_result and 'access' in login_result:
                test_me_endpoint(login_result['access'])
        
        print_section("TEST SUMMARY")
        print("All tests completed! Check results above.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the backend server is running!")

if __name__ == "__main__":
    main()
