# IK Recruitment Platform

A modern, modular, and scalable recruitment platform for managing hiring processes.

## Table of Contents
- [Tech Stack & Architecture](#tech-stack--architecture)
- [Setup & Running](#setup--running)
- [Services & Modules](#services--modules)
- [Logging & Monitoring](#logging--monitoring)
- [API Reference](#api-reference)
- [Developer Notes](#developer-notes)
- [License](#license)

---

## Tech Stack & Architecture

**Backend:**
- Python 3.10+
- Django 5.2
- Django REST Framework
- Celery (asynchronous task queue)
- PostgreSQL (database)
- Redis (cache & Celery broker)
- Flower (Celery monitoring)
- ELK Stack (Elasticsearch, Logstash, Kibana) — Advanced logging & monitoring

**Other:**
- Docker & Docker Compose (for easy setup)
- JWT Authentication (djangorestframework-simplejwt)
- Environment-based configuration
- Internationalization (i18n, rosetta)

---

## Setup & Running

### 1. Requirements
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)

### 2. Clone the Project
```bash
git clone <repo-url>
cd IK
```

### 3. Start All Services
```bash
docker compose up -d --build
```
Services started:
- Django Web (8000)
- PostgreSQL (5432)
- Redis (6379)
- Celery Worker & Beat
- Flower (5555)
- Elasticsearch (9200)
- Logstash (5959)
- Kibana (5601)

### 4. Apply Migrations
```bash
docker compose exec web python manage.py migrate
```

### 5. Create Admin User
```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Access the Application
- Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- API: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
- Flower: [http://localhost:5555](http://localhost:5555)
- Kibana: [http://localhost:5601](http://localhost:5601)

### 7. Load Sample Data (for development/testing)
```bash
docker compose exec web python manage.py generate_fake_data
```

---

## Services & Modules

- **apps/candidate:** Candidate management
- **apps/client_company:** Client company management
- **apps/flow:** Candidate process & activity management
- **apps/hr_company:** HR company management
- **apps/hr_user:** HR user management
- **apps/job_posting:** Job posting management
- **apps/api:** API endpoints & versioning

Each app contains a `docs/readme.md` file with detailed explanations.

---

## Logging & Monitoring

- **Logging:** Django logs are written in JSON format to a file and shipped to Elasticsearch via Logstash.
- **Kibana:** Visualize and search logs at [http://localhost:5601](http://localhost:5601).
- **Flower:** Monitor Celery tasks and queues at [http://localhost:5555](http://localhost:5555).

---

## API Reference

### Authentication

#### JWT Authentication

- **Login:**
  `POST /api/v1/auth/login/jwt`
  Request:
  ```json
  { "email": "test@example.com", "password": "test123" }
  ```
  Response:
  ```json
  {
    "user": { ... },
    "tokens": { "access": "...", "refresh": "..." }
  }
  ```

- **Token Refresh:**
  `POST /api/v1/auth/refresh/jwt`
  Request:
  ```json
  { "refresh": "..." }
  ```
  Response:
  ```json
  { "access": "..." }
  ```

- **Usage:**
  Add the access token to the `Authorization` header as `Bearer <token>`.

#### Session Authentication

- **Login:**
  `POST /api/v1/auth/login/session`
  Request:
  ```json
  { "email": "test@example.com", "password": "test123" }
  ```
  Response:
  ```json
  {
    "user": { ... },
    "message": "Login successful"
  }
  ```

- **Logout:**
  `POST /api/v1/auth/logout/session`
  Response:
  ```json
  { "message": "Logout successful" }
  ```

---

### Main API Endpoints

#### Candidates

- `GET /api/v1/candidates/` — List all candidates (with filtering)
- `POST /api/v1/candidates/` — Create a new candidate
- `GET /api/v1/candidates/{id}/` — Retrieve candidate details
- `PUT/PATCH /api/v1/candidates/{id}/` — Update candidate
- `DELETE /api/v1/candidates/{id}/` — Delete candidate

- `GET/POST /api/v1/candidates/{id}/educations/` — List or add education records for a candidate
- `GET/POST /api/v1/candidates/{id}/work_experiences/` — List or add work experiences for a candidate

#### Educations

- `GET /api/v1/educations/` — List all education records (filterable by candidate)
- `POST /api/v1/educations/` — Create a new education record

#### Work Experiences

- `GET /api/v1/work-experiences/` — List all work experiences (filterable by candidate)
- `POST /api/v1/work-experiences/` — Create a new work experience

#### Job Postings

- `GET /api/v1/job-postings/` — List all job postings
- `POST /api/v1/job-postings/` — Create a new job posting
- `GET /api/v1/job-postings/{id}/` — Retrieve job posting details
- `PUT/PATCH /api/v1/job-postings/{id}/` — Update job posting
- `DELETE /api/v1/job-postings/{id}/` — Delete job posting
- `POST /api/v1/job-postings/{id}/activate/` — Activate a job posting
- `POST /api/v1/job-postings/{id}/deactivate/` — Deactivate a job posting

#### HR Users

- `GET /api/v1/hr-users/` — List all HR users
- `POST /api/v1/hr-users/` — Create a new HR user
- `GET /api/v1/hr-users/{id}/` — Retrieve HR user details
- `PUT/PATCH /api/v1/hr-users/{id}/` — Update HR user
- `DELETE /api/v1/hr-users/{id}/` — Delete HR user

---

## Developer Notes

- All configuration is managed via `.env` or `docker-compose.yml` environment variables.
- Run migrations and collect static files manually if needed.
- For each module, see `apps/<module>/docs/readme.md`.
- For authentication and JWT details, see `AUTHENTICATION_README.md`.

---

## License

This project is licensed under the MIT License.

---

If you encounter any issues, check the logs or inspect service status with `docker compose ps`.
