import requests

BASE_URL = "http://localhost:8000/api"

def test_exam():
    # 0. Register User (if not exists)
    print("Registering User...")
    reg_data = {"username": "testuser_v3", "password": "password123", "email": "test3@example.com"}
    try:
        requests.post(f"{BASE_URL}/auth/register/", json=reg_data)
    except:
        pass

    # 1. Login
    print("Logging in...")
    login_data = {"username": "testuser_v3", "password": "password123"}
    try:
        res = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        if res.status_code != 200:
            print(f"Login Failed: {res.text}")
            return
        token = res.json()['access']
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"Login Error: {e}")
        return

    # 2. Get First Test ID
    print("\nFetching Tests...")
    try:
        tests = requests.get(f"{BASE_URL}/tests/", headers=headers).json()
        if not tests:
            print("No tests found.")
            return
        test_id = tests[0]['id']
        print(f"Starting Test ID: {test_id}")
    except Exception as e:
        print(f"Fetch Error: {e}")
        return

    # 3. Start Test
    print("\nStarting Test...")
    try:
        res = requests.post(f"{BASE_URL}/exam/start/{test_id}/", headers=headers)
        data = res.json()
        attempt_id = data['attempt_id']
        questions = data['questions']
        print(f"Attempt ID: {attempt_id}")
        print(f"Received {len(questions)} questions.")
    except Exception as e:
        print(f"Start Error: {e}")
        print(f"Response Text: {res.text}")
        return

    # 4. Submit Answer (Correct)
    print("\nSubmitting Answer...")
    q1 = questions[0]
    try:
        res = requests.post(f"{BASE_URL}/exam/submit-answer/", json={
            "attempt_id": attempt_id,
            "question_id": q1['id'],
            "selected_option": "A" 
        }, headers=headers)
        print(f"Answer Submit Status: {res.status_code}")
    except Exception as e:
        print(f"Answer Error: {e}")

    # 5. Submit Test
    print("\nSubmitting Test...")
    try:
        res = requests.post(f"{BASE_URL}/exam/submit/", json={
            "attempt_id": attempt_id
        }, headers=headers)
        print(f"Test Submit Response: {res.json()}")
    except Exception as e:
        print(f"Submit Error: {e}")

if __name__ == "__main__":
    test_exam()
