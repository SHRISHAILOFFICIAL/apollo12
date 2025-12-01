import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

def test_auth():
    # 1. Register
    print("Testing Registration...")
    reg_data = {
        "username": "testuser_v2",
        "password": "password123",
        "email": "test2@example.com"
    }
    try:
        res = requests.post(f"{BASE_URL}/register/", json=reg_data)
        print(f"Register Status: {res.status_code}")
        print(f"Register Response: {res.text}")
    except Exception as e:
        print(f"Register Failed: {e}")

    # 2. Login
    print("\nTesting Login...")
    login_data = {
        "username": "testuser_v2",
        "password": "password123"
    }
    try:
        res = requests.post(f"{BASE_URL}/login/", json=login_data)
        print(f"Login Status: {res.status_code}")
        if res.status_code == 200:
            print("Login Success! Token received.")
        else:
            print(f"Login Failed: {res.text}")
    except Exception as e:
        print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_auth()
