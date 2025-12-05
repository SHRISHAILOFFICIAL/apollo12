"""
Test script to verify all API endpoints
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

def print_section(message):
    print(f"\n{Colors.YELLOW}{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}{Colors.END}")

# Test data
test_user = {
    "email": f"test_{datetime.now().timestamp()}@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User",
    "mobile_number": f"987654{int(datetime.now().timestamp()) % 10000}"
}

def test_user_registration():
    print_section("Testing User Registration")
    try:
        response = requests.post(f"{BASE_URL}/users/register/", json=test_user)
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success("User registration successful!")
            print_info(f"User ID: {data.get('user', {}).get('id')}")
            print_info(f"Email: {data.get('user', {}).get('email')}")
            if 'access' in data:
                print_info("JWT tokens received")
                return data
        else:
            print_error(f"Registration failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error during registration: {str(e)}")
        return None

def test_user_login():
    print_section("Testing User Login")
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Login successful!")
            print_info(f"Access token received: {data.get('access')[:20]}...")
            return data
        else:
            print_error(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error during login: {str(e)}")
        return None

def test_user_profile(token):
    print_section("Testing User Profile")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/profile/", headers=headers)
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Profile retrieved successfully!")
            print_info(f"User: {data.get('first_name')} {data.get('last_name')}")
            print_info(f"Email: {data.get('email')}")
            return data
        else:
            print_error(f"Profile retrieval failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error retrieving profile: {str(e)}")
        return None

def test_subjects_list(token):
    print_section("Testing Subjects List")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/subjects/", headers=headers)
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {len(data)} subjects")
            for subject in data[:3]:
                print_info(f"- {subject.get('name')}")
            return data
        else:
            print_error(f"Subjects retrieval failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error retrieving subjects: {str(e)}")
        return None

def test_exams_list(token):
    print_section("Testing Exams List")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/exams/", headers=headers)
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {len(data)} exams")
            for exam in data[:3]:
                print_info(f"- {exam.get('title')}")
            return data
        else:
            print_error(f"Exams retrieval failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error retrieving exams: {str(e)}")
        return None

def test_notifications(token):
    print_section("Testing Notifications")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/notifications/", headers=headers)
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Retrieved {len(data)} notifications")
            return data
        else:
            print_error(f"Notifications retrieval failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error retrieving notifications: {str(e)}")
        return None

def main():
    print("\n" + "="*60)
    print("  QUIZ PLATFORM API TEST SUITE")
    print("="*60 + "\n")
    
    # Test user registration
    reg_data = test_user_registration()
    if not reg_data:
        print_error("Registration failed. Cannot proceed with other tests.")
        return
    
    token = reg_data.get('access')
    
    # Test user login
    login_data = test_user_login()
    if login_data:
        token = login_data.get('access')
    
    # Test authenticated endpoints
    if token:
        test_user_profile(token)
        test_subjects_list(token)
        test_exams_list(token)
        test_notifications(token)
    
    print_section("Test Summary")
    print_info("API testing completed!")
    print_info(f"Base URL: {BASE_URL}")
    print_info("Check the results above for any failures.\n")

if __name__ == "__main__":
    main()
