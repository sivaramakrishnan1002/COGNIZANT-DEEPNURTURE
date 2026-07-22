# Hands-On 10: Microservices Architecture — Concepts & Decomposition

## Overview
This directory contains the microservices decomposition of the Course Management API into independent Flask microservices, behind a lightweight API Gateway proxy.

---

## Task 1: Microservice Boundaries & Decomposition

### 1. Bounded Context Identification (Decomposition Table)

| Service Name | Responsibility | Endpoints Owned | Database Owned |
| :--- | :--- | :--- | :--- |
| **Student Service** | Manages student profiles, student CRUD, and course enrollment records. | `GET /api/students`<br>`GET /api/students/{id}`<br>`POST /api/students`<br>`PUT /api/students/{id}`<br>`DELETE /api/students/{id}`<br>`POST /api/students/{id}/enroll`<br>`GET /api/students/{id}/enrollments` | `students.db`<br>*(Tables: `students`, `enrollments`)* |
| **Course Service** | Manages course catalog details, credit information, and academic departments. | `GET /api/courses`<br>`GET /api/courses/{id}`<br>`POST /api/courses`<br>`PUT /api/courses/{id}`<br>`DELETE /api/courses/{id}`<br>`GET /api/departments`<br>`GET /api/departments/{id}`<br>`POST /api/departments`<br>`PUT /api/departments/{id}`<br>`DELETE /api/departments/{id}` | `courses.db`<br>*(Tables: `courses`, `departments`)* |
| **Auth Service** *(Planned)* | User registration, authentication, password hashing, and JWT token issuance/validation. | `POST /api/auth/register`<br>`POST /api/auth/login`<br>`POST /api/auth/verify` | `auth.db`<br>*(Tables: `users`, `tokens`)* |
| **Notification Service** *(Planned)* | Handles email notifications, enrollment confirmations, and status alerts asynchronously. | `POST /api/notifications/send-email`<br>`GET /api/notifications/logs` | `notifications.db`<br>*(Tables: `notification_logs`)* |

### 2. Microservice Isolation Principles
- **Data Autonomy**: Each microservice strictly owns its database (SQLite databases `courses.db` and `students.db` are isolated in `course_service/` and `student_service/` respectively).
- **No Shared Databases**: `student_service` does NOT query `courses.db` directly. Instead, when student enrollment requires validating a course, `student_service` performs a synchronous HTTP GET request to `course_service`.
- **Independent Ports**:
  - API Gateway: **Port 5000**
  - Course Service: **Port 5001**
  - Student Service: **Port 5002**

---

## Task 2: Inter-Service Communication & API Gateway

### 1. Verification Flow
1. Client sends request to API Gateway:
   `POST http://localhost:5000/api/students/1/enroll` with JSON `{"course_id": 1}`.
2. Gateway routes request to Student Service (`http://localhost:5002/api/students/1/enroll`).
3. Student Service receives enrollment request and calls Course Service (`GET http://localhost:5001/api/courses/1`).
4. Course Service verifies course exists and returns 200 OK with course details.
5. Student Service records enrollment in `students.db` and returns HTTP 201 Created.
6. **Failure Handling**: If Course Service is down/offline when an enrollment is requested, Student Service catches `requests.exceptions.RequestException` and returns `503 Service Unavailable` with `{"error": "Course Service Unavailable"}`.

---

## Architecture Deep-Dive: Inter-Service Communication Trade-offs

### Synchronous (HTTP / REST) vs Asynchronous (Message Queue e.g., RabbitMQ / Kafka)

| Dimension | Synchronous (HTTP / REST) | Asynchronous (Message Queue) |
| :--- | :--- | :--- |
| **Coupling** | **Tight Coupling**: Requesting service depends directly on the immediate availability of the downstream service. | **Loose Coupling**: Services communicate via messages/events published to a broker. |
| **Availability / Fault Tolerance** | **Low Fault Tolerance**: If Course Service is down, Student Service enrollment immediately fails (returns HTTP 503). | **High Fault Tolerance**: Messages are queued. If consumer service is down, messages wait in queue and are processed when service recovers. |
| **Latency & Response** | **Blocking**: Client waits for request-response cycle across multiple network hops. | **Non-blocking**: Instant response to client after publishing message to broker. |
| **Consistency Model** | **Immediate Consistency**: Validations happen instantly during the API call. | **Eventual Consistency**: State updates across services happen asynchronously over time. |
| **Operational Complexity** | **Low**: Standard REST APIs, easy to implement, debug, and trace with basic HTTP toolkits. | **Higher**: Requires setting up broker infrastructure (RabbitMQ/Kafka), retry queues, dead-letter exchanges, idempotency handlers. |

### When to Use a Message Queue (RabbitMQ / Kafka)?
1. **Background & Heavy Processing**: When completing a user action takes time (e.g. sending enrollment confirmation emails, generating PDF certificates, video encoding).
2. **High Throughput / Event Streaming**: In streaming architectures (e.g. tracking user activity, analytics, audit logging) where Kafka excels at log retention and high-ingestion throughput.
3. **Decoupling Core Workflows**: When multiple downstream services need to react to a single event without clogging the main API endpoint (e.g., when a student enrolls, publish `StudentEnrolled` event so Notification Service, Billing Service, and Analytics Service process it independently).
4. **Resilience to Outages**: When downstream services may experience temporary downtime or variable spikes in traffic, queues absorb the load.
