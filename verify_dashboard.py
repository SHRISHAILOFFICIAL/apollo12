import requests

BASE_URL = "http://localhost:8000/api"

def test_dashboard():
    # 1. Login to get token
    print("Logging in...")
    login_data = {
        "username": "testuser_v2",
        "password": "password123"
    }
    try:
        res = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if res.status_code != 200:
            print(f"Login Failed: {res.text}")
            return
        token = res.json()['access']
        print("Login Success.")
    except Exception as e:
        print(f"Login Error: {e}")
        return

    # 2. Fetch Tests
    print("\nFetching Tests...")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(f"{BASE_URL}/tests/", headers=headers)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            tests = res.json()
            print(f"Found {len(tests)} tests.")
            for t in tests:
                print(f"- {t['title']} ({t['total_marks']} Marks)")
        else:
            print(f"Failed: {res.text}")
    except Exception as e:
        print(f"Fetch Error: {e}")

if __name__ == "__main__":
    test_dashboard()
