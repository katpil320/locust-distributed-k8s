"""
Simple HTTP Load Test Example

This is a basic example of a Locust test that can be used to test any HTTP endpoint.
To use this script:
1. Upload this file as 'locustfile.py' to the shared storage via File Browser
2. Scale up the Locust master and workers
3. Configure the target host in the Locust web UI
4. Start your load test

This script simulates users browsing a website with different endpoints.
"""

from locust import HttpUser, task, between
import random


class WebsiteUser(HttpUser):
    """
    A user class that simulates typical website browsing behavior.
    
    The wait_time defines how long a user waits between tasks (1-5 seconds).
    """
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Called when a user starts. You can use this for login or setup tasks.
        """
        # Example: Login or get session token
        pass
    
    @task(3)
    def view_homepage(self):
        """
        Simulate viewing the homepage.
        Weight of 3 means this task is 3x more likely to be executed.
        """
        self.client.get("/")
    
    @task(2)
    def view_about_page(self):
        """
        Simulate viewing an about page.
        """
        self.client.get("/about")
    
    @task(1)
    def view_contact_page(self):
        """
        Simulate viewing a contact page.
        """
        self.client.get("/contact")
    
    @task(2)
    def search(self):
        """
        Simulate performing a search.
        """
        search_terms = ["product", "service", "help", "pricing", "demo"]
        term = random.choice(search_terms)
        self.client.get(f"/search?q={term}")
    
    @task(1)
    def submit_form(self):
        """
        Simulate submitting a form with POST request.
        """
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "This is a test message from Locust load testing"
        }
        self.client.post("/contact", data=data)


class APIUser(HttpUser):
    """
    Example API user for testing REST endpoints.
    You can have multiple user classes in the same file.
    """
    wait_time = between(0.5, 2)
    
    @task
    def get_users(self):
        """Test GET endpoint for users."""
        self.client.get("/api/users")
    
    @task
    def get_user_by_id(self):
        """Test GET endpoint for specific user."""
        user_id = random.randint(1, 100)
        self.client.get(f"/api/users/{user_id}")
    
    @task
    def create_user(self):
        """Test POST endpoint to create user."""
        user_data = {
            "name": f"User{random.randint(1, 1000)}",
            "email": f"user{random.randint(1, 1000)}@example.com"
        }
        self.client.post("/api/users", json=user_data)
