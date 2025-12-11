"""
SIMPLIFIED Load Test - Tests only what exists
"""
from locust import HttpUser, task, between

class SimpleUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_api_root(self):
        """Test if API is responding"""
        self.client.get("/api/")
    
    @task
    def test_exams_list(self):
        """Test exams endpoint"""
        self.client.get("/api/exams/")
