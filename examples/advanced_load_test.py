"""
Advanced Load Test Example with Custom Load Shapes

This example demonstrates:
- Custom load shapes (gradual ramp-up, spike testing, etc.)
- Data-driven testing (reading from files)
- Custom user behavior patterns
- Error handling and validation

To use this script:
1. Upload this file as 'locustfile.py' to the shared storage
2. Also upload the 'test_data.json' file (example included below)
3. Scale up Locust master and workers
4. Start your test from the web UI
"""

from locust import HttpUser, task, between, LoadTestShape
import json
import random
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedWebUser(HttpUser):
    """
    Advanced user simulation with data-driven testing.
    """
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Initialize user with test data.
        Load test data from JSON file if available.
        """
        try:
            with open('/mnt/locust/test_data.json', 'r') as f:
                self.test_data = json.load(f)
                logger.info("Loaded test data successfully")
        except FileNotFoundError:
            # Fallback data if file doesn't exist
            self.test_data = {
                "users": [
                    {"username": "testuser1", "password": "password123"},
                    {"username": "testuser2", "password": "password456"}
                ],
                "products": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
            logger.warning("Test data file not found, using fallback data")
        
        # Login once per user session
        self.login()
    
    def login(self):
        """
        Perform login with random user credentials.
        """
        user = random.choice(self.test_data["users"])
        response = self.client.post("/login", data={
            "username": user["username"],
            "password": user["password"]
        })
        
        if response.status_code == 200:
            logger.info(f"Successfully logged in as {user['username']}")
        else:
            logger.error(f"Login failed for {user['username']}")
    
    @task(5)
    def browse_products(self):
        """
        Browse product listings with pagination.
        """
        page = random.randint(1, 5)
        response = self.client.get(f"/products?page={page}")
        
        # Validate response
        if response.status_code == 200 and "products" in response.text:
            logger.debug("Successfully browsed products")
        else:
            logger.warning(f"Unexpected response when browsing products: {response.status_code}")
    
    @task(3)
    def view_product_details(self):
        """
        View detailed product page.
        """
        product_id = random.choice(self.test_data["products"])
        response = self.client.get(f"/products/{product_id}")
        
        if response.status_code == 200:
            # Simulate reading time
            self.wait()
    
    @task(2)
    def add_to_cart(self):
        """
        Add random product to shopping cart.
        """
        product_id = random.choice(self.test_data["products"])
        quantity = random.randint(1, 3)
        
        response = self.client.post("/cart/add", data={
            "product_id": product_id,
            "quantity": quantity
        })
        
        if response.status_code == 200:
            logger.debug(f"Added product {product_id} to cart")
    
    @task(1)
    def checkout_process(self):
        """
        Simulate going through checkout process.
        """
        # View cart
        self.client.get("/cart")
        
        # Go to checkout
        response = self.client.get("/checkout")
        if response.status_code == 200:
            # Simulate filling out form (don't actually complete purchase)
            self.client.post("/checkout/validate", data={
                "email": "test@example.com",
                "address": "123 Test St",
                "city": "Test City"
            })


class StressTestShape(LoadTestShape):
    """
    Custom load shape for stress testing.
    
    This shape:
    1. Ramps up to 50 users over 2 minutes
    2. Maintains 50 users for 3 minutes  
    3. Spikes to 200 users for 1 minute
    4. Drops back to 50 users for 2 minutes
    5. Ramps down to 0 over 1 minute
    """
    
    stages = [
        {"duration": 120, "users": 50, "spawn_rate": 1},     # Ramp up
        {"duration": 300, "users": 50, "spawn_rate": 1},     # Steady state
        {"duration": 360, "users": 200, "spawn_rate": 10},   # Spike
        {"duration": 480, "users": 50, "spawn_rate": 5},     # Back down
        {"duration": 540, "users": 0, "spawn_rate": 2},      # Ramp down
    ]
    
    def tick(self):
        """
        Define the load shape behavior at each time tick.
        """
        run_time = self.get_run_time()
        
        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])
        
        # Test complete
        return None


# Alternative load shape classes you can use:

class GradualRampShape(LoadTestShape):
    """
    Gradual ramp-up over 10 minutes to 100 users.
    """
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time < 600:  # 10 minutes
            # Gradual increase: 1 user every 6 seconds
            user_count = int(run_time / 6)
            return (min(user_count, 100), 1)
        
        return (100, 1)  # Maintain 100 users


class SpikeTestShape(LoadTestShape):
    """
    Spike test: quick ramp to high load, then back down.
    """
    def tick(self):
        run_time = self.get_run_time()
        
        if run_time < 60:
            return (10, 2)  # Start with 10 users
        elif run_time < 120:
            return (500, 20)  # Spike to 500 users quickly
        elif run_time < 180:
            return (10, 10)  # Back down quickly
        else:
            return None  # End test
