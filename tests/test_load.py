"""
Load Testing with Locust
Simulate concurrent users and measure performance
"""

from locust import HttpUser, task, between
import json
import random


class ChatBotUser(HttpUser):
    """Simulated user interacting with chatbot"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    def on_start(self):
        """Called when a user starts"""
        self.session_id = f"load-test-{self.environment.runner.user_count}-{random.randint(1000, 9999)}"
        self.messages = [
            "Hello",
            "What courses do you offer?",
            "Tell me about Python programming",
            "What are the admission requirements?",
            "How do I register?",
            "What is the fee structure?",
            "Tell me about scholarships",
            "What is machine learning?",
            "Explain artificial intelligence",
            "How can I contact support?"
        ]
    
    @task(10)
    def send_message(self):
        """Send chat message (most common task)"""
        message = random.choice(self.messages)
        
        self.client.post("/api/chat", json={
            "message": message,
            "session_id": self.session_id
        }, name="Send Chat Message")
    
    @task(3)
    def get_autocomplete(self):
        """Get autocomplete suggestions"""
        queries = ["wha", "how", "tel", "exp"]
        query = random.choice(queries)
        
        self.client.get(f"/api/autocomplete?q={query}&limit=5", 
                       name="Get Autocomplete")
    
    @task(2)
    def get_chat_history(self):
        """Get chat history"""
        self.client.get("/api/chat/history", 
                       name="Get Chat History")
    
    @task(1)
    def save_context(self):
        """Save conversation context"""
        self.client.post("/api/context/save", json={
            "session_id": self.session_id,
            "context_data": {
                "topic": random.choice(["courses", "admission", "fees"]),
                "intent": "inquiry"
            }
        }, name="Save Context")
    
    @task(1)
    def get_context(self):
        """Get conversation context"""
        self.client.get(f"/api/context/{self.session_id}", 
                       name="Get Context")


class AdminUser(HttpUser):
    """Simulated admin user"""
    
    wait_time = between(3, 7)
    
    @task(5)
    def view_analytics(self):
        """View analytics dashboard"""
        self.client.get("/api/analytics/dashboard", 
                       name="View Analytics")
    
    @task(3)
    def view_all_conversations(self):
        """View all conversations"""
        self.client.get("/api/admin/conversations", 
                       name="View All Conversations")
    
    @task(2)
    def get_user_stats(self):
        """Get user statistics"""
        self.client.get("/api/analytics/users", 
                       name="Get User Stats")
    
    @task(1)
    def export_data(self):
        """Export data"""
        self.client.get("/api/admin/export", 
                       name="Export Data")


class GuestUser(HttpUser):
    """Simulated guest (unauthenticated) user"""
    
    wait_time = between(2, 5)
    
    def on_start(self):
        self.session_id = f"guest-{random.randint(1000, 9999)}"
    
    @task(10)
    def send_message_guest(self):
        """Send message as guest"""
        messages = [
            "Hello",
            "What can you help me with?",
            "Tell me about your services"
        ]
        
        self.client.post("/api/chat", json={
            "message": random.choice(messages),
            "session_id": self.session_id
        }, name="Guest Send Message")
    
    @task(5)
    def view_home_page(self):
        """View home page"""
        self.client.get("/", name="View Home Page")
    
    @task(2)
    def view_about_page(self):
        """View about page"""
        self.client.get("/about", name="View About Page")


class APILoadTest(HttpUser):
    """Test API endpoints under load"""
    
    wait_time = between(0.5, 2)
    
    @task
    def test_chat_endpoint(self):
        """Test chat endpoint performance"""
        self.client.post("/api/chat", json={
            "message": "Performance test message",
            "session_id": f"perf-{random.randint(1, 100)}"
        }, name="Chat API Performance")
    
    @task
    def test_autocomplete_endpoint(self):
        """Test autocomplete performance"""
        self.client.get("/api/autocomplete?q=test&limit=10", 
                       name="Autocomplete Performance")
    
    @task
    def test_context_endpoint(self):
        """Test context save performance"""
        self.client.post("/api/context/save", json={
            "session_id": f"perf-{random.randint(1, 100)}",
            "context_data": {"test": "data"}
        }, name="Context Save Performance")


# Load test scenarios
class StressTest(HttpUser):
    """Stress test with high load"""
    
    wait_time = between(0.1, 0.5)  # Very short wait time
    
    @task
    def rapid_fire_messages(self):
        """Send messages rapidly"""
        self.client.post("/api/chat", json={
            "message": f"Stress test {random.randint(1, 10000)}",
            "session_id": "stress-test"
        }, name="Stress Test Message")


class SpikeTest(HttpUser):
    """Spike test - sudden load increase"""
    
    wait_time = between(0.1, 1)
    
    @task
    def spike_load(self):
        """Generate spike in traffic"""
        # Send multiple requests
        for _ in range(5):
            self.client.post("/api/chat", json={
                "message": "Spike test",
                "session_id": "spike-test"
            }, name="Spike Test")


class EnduranceTest(HttpUser):
    """Endurance test - sustained load"""
    
    wait_time = between(1, 2)
    
    @task
    def sustained_load(self):
        """Maintain sustained load"""
        self.client.post("/api/chat", json={
            "message": "Endurance test message",
            "session_id": "endurance-test"
        }, name="Endurance Test")


# Run with:
# locust -f tests/test_load.py --host=http://localhost:5000 --users=100 --spawn-rate=10
