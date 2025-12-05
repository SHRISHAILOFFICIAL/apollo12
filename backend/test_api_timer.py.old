"""
Test the actual API endpoint for starting an exam with timer
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("=" * 60)
print("TESTING EXAM TIMER API ENDPOINTS")
print("=" * 60)

# Step 1: Login to get token
print("\n1. Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login/",
    json={"username": "sonu", "password": "sonu"}
)

if login_response.status_code == 200:
    token_data = login_response.json()
    access_token = token_data.get("access")
    print(f"✅ Login successful!")
    print(f"   Token: {access_token[:30]}...")
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Step 2: Start exam with timer
print("\n2. Starting exam with timer...")
start_response = requests.post(
    f"{BASE_URL}/exam/timer/start/1/",
    headers=headers
)

print(f"Status Code: {start_response.status_code}")
print(f"Response: {json.dumps(start_response.json(), indent=2)}")

if start_response.status_code in [200, 201]:
    attempt_data = start_response.json()
    attempt_id = attempt_data.get("attempt_id")
    print(f"✅ Exam started successfully!")
    print(f"   Attempt ID: {attempt_id}")
    print(f"   Remaining: {attempt_data.get('remaining_seconds')}s")
    
    # Step 3: Check remaining time
    print("\n3. Checking remaining time...")
    remaining_response = requests.get(
        f"{BASE_URL}/exam/timer/remaining/{attempt_id}/",
        headers=headers
    )
    
    print(f"Status Code: {remaining_response.status_code}")
    print(f"Response: {json.dumps(remaining_response.json(), indent=2)}")
    
    if remaining_response.status_code == 200:
        remaining_data = remaining_response.json()
        print(f"✅ Timer check successful!")
        print(f"   Status: {remaining_data.get('status')}")
        print(f"   Remaining: {remaining_data.get('remaining_seconds')}s")
        
        print("\n" + "=" * 60)
        print("✅ TIMER API WORKING!")
        print("=" * 60)
        print(f"\nNow check in WSL Redis:")
        print(f"  redis-cli")
        print(f"  SELECT 1")
        print(f"  KEYS exam:timer:*")
        print(f"  TTL exam:timer:{attempt_id}")
        print(f"  GET exam:timer:{attempt_id}")
    else:
        print(f"❌ Timer check failed: {remaining_response.status_code}")
        print(remaining_response.text)
else:
    print(f"❌ Exam start failed: {start_response.status_code}")
    print(start_response.text)
