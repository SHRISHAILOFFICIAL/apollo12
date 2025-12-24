"""
Load testing script for Apollo11 DCET Platform
Matches actual API endpoints from your Django backend
"""
from locust import HttpUser, task, between
import random

class ExamUser(HttpUser):
    wait_time = between(2, 5)  # Realistic user think time
    token = None
    
    def on_start(self):
        """Login before starting test - using actual auth endpoints"""
        # Try to login with existing test user
        with self.client.post("/api/users/auth/login/", json={
            "username": "testuser",
            "password": "testpass123"
        }, name="Login", catch_response=True) as response:
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access", "")
                response.success()
            else:
                # If login fails, that's expected (user doesn't exist yet)
                response.failure(f"Login failed: {response.status_code}")
                self.token = None
    
    @task(5)  # Most common action - loading exams list
    def load_exams_list(self):
        """Simulate loading list of exams"""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        with self.client.get("/api/exams/", headers=headers, catch_response=True, name="Load Exams List") as response:
            if response.status_code in [200, 401]:  # 401 is ok (not logged in)
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(3)  # Loading specific exam
    def load_exam_detail(self):
        """Simulate loading a specific exam"""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        exam_id = random.randint(1, 5)  # Assuming you have exams 1-5
        with self.client.get(f"/api/exams/{exam_id}/", headers=headers, catch_response=True, name="Load Exam Detail") as response:
            if response.status_code in [200, 404, 401]:  # 404 ok if exam doesn't exist
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(2)  # Viewing results
    def view_results(self):
        """Simulate viewing exam results"""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        with self.client.get("/api/results/", headers=headers, catch_response=True, name="View Results") as response:
            if response.status_code in [200, 401]:
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(1)  # Homepage/API root
    def api_root(self):
        """Test API root endpoint"""
        with self.client.get("/api/", catch_response=True, name="API Root") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"API root failed: {response.status_code}")

