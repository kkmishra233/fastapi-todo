from locust import HttpUser, task, between, events
import random
import gevent

class TodoUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    def on_start(self):
        """Ensures all users start simultaneously."""
        global all_users_ready
        all_users_ready.wait()

    @task(2)
    def list_todos(self):
        self.client.get("/todos")

    @task(3)
    def create_todo(self):
        todo = {"title": f"Test Todo {random.randint(1, 1000)}", "description": "This is a test todo."}
        response = self.client.post("/todos", json=todo)
        if response.status_code == 201:
            todo_id = response.json().get("id")
            self.update_todo(todo_id)
            self.delete_todo(todo_id)

    def update_todo(self, todo_id):
        updated_todo = {"title": "Updated Todo", "description": "Updated description."}
        self.client.put(f"/todos/{todo_id}", json=updated_todo)

    def delete_todo(self, todo_id):
        self.client.delete(f"/todos/{todo_id}")

# Global event to synchronize user start
all_users_ready = gevent.event.Event()

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """Set number of users and make sure all start together."""
    if not environment.parsed_options:
        return

    environment.parsed_options.num_users = 1000   # Set number of users
    environment.parsed_options.spawn_rate = 10  # All users start at once

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Trigger all users to start at the same time."""
    all_users_ready.set()
    gevent.spawn_later(300, environment.runner.quit) # 300 seconds = 5 minutes
