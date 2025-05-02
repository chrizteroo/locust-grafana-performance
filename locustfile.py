from locust import HttpUser, task, between
from prometheus_client import start_http_server, Counter

# Expose Prometheus metrics on port 9091
start_http_server(9091)

# Optional: count total requests
REQUEST_COUNT = Counter("locust_requests_total", "Total HTTP requests")

class StudentPortalUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def download_student_id(self):
        REQUEST_COUNT.inc()
        self.client.get("/api/student/id", name="Download ID")

    @task(2)
    def download_transcript(self):
        REQUEST_COUNT.inc()
        self.client.post("/api/transcript/download",
                         json={"studentId": "12345"},
                         name="Download Transcript")

    @task(1)
    def approve_transcript(self):
        REQUEST_COUNT.inc()
        self.client.put("/api/transcript/approve",
                        json={"transcriptId": "67890"},
                        name="Approve Transcript")
