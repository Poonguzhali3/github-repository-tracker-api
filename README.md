GitHub Repository Tracker API

Problem Understanding & Assumptions


The goal of this project is to build a robust REST API using FastAPI and PostgreSQL that acts as a bridge between a local database and an external API. The service demonstrates proper state management, strict validation, error handling, and testing.

Use Case:

GitHub Repository Tracker API
The API allows users to store and manage GitHub repository metadata. When a repository is created, additional details (stars, language, description) are fetched from the GitHub public API and persisted locally.

*Assumptions

* GitHub public API is accessible without authentication for basic repository data
* No user authentication is required for this assessment
* Repository owner and name uniquely identify a GitHub repository
* Rate limiting and GitHub outages are possible and must be handled gracefully
* PostgreSQL is running locally during development

---

#Design Decisions

#Database Schema

A single `repositories` table is used with the following fields:

* `id` (Primary Key)
* `owner`
* `repo_name`
* `stars`
* `language`
* `description`
* `created_at`
* `updated_at`

Indexes are implicitly handled via the primary key.

#Project Structure


API_PROJECT/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── github_client.py
│   └── exceptions.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_github_client.py
├── .env
├── requirements.txt
└── README.md


A layered approach is used to separate concerns (API, DB, external services).

# Validation Logic

* Pydantic models validate all request and response payloads
* Partial updates are supported using optional fields
* Invalid inputs return `422 Unprocessable Entity`

# External API Design

* GitHub API is accessed using `httpx.AsyncClient`
* Timeouts are configured to prevent blocking
* External failures return `503 Service Unavailable`


#Solution Approach (Data Flow)

1. Client sends request to FastAPI endpoint
2. Request is validated using Pydantic
3. For creation, GitHub API is called to fetch repository details
4. Data is stored in PostgreSQL using SQLAlchemy
5. Response is returned using response schemas

#Error Handling Strategy

Global exception handlers are implemented for:

* Database errors → 500 Internal Server Error
* External API failures →503 Service Unavailable
* Unexpected errors →500 Internal Server Error

This ensures the application does not crash and always returns meaningful responses.

# How to Run the Project

#Setup Virtual Environment
bash
python -m venv .venv
.venv\\Scripts\\activate
Install Dependencies
bash
pip install -r requirements.txt

#Environment Variables

Create a .env file:

DATABASE_URL=postgresql://postgres:<password>@localhost:5432/github_db
GITHUB_API_BASE=https://api.github.com


#Run the Application

bash
python -m uvicorn app.main:app --reload

# Swagger Documentation

Open:

http://127.0.0.1:8000/docs

#API Endpoints

| Method | Endpoint           | Description                                |
| ------ | ------------------ | ------------------------------------------ |
| POST   | /repositories      | Create repository (GitHub API integration) |
| GET    | /repositories/{id} | Fetch repository                           |
| PUT    | /repositories/{id} | Update repository                          |
| DELETE | /repositories/{id} | Delete repository                          |



#Testing

#Run Tests
bash
pytest

#Test Coverage

* Unit Tests: External GitHub API logic (mocked)
* Integration Tests: FastAPI endpoints

External APIs are mocked to ensure deterministic and reliable test results.


 Conclusion

This project demonstrates clean architecture, proper error handling, external API integration, and reliable automated testing using FastAPI and PostgreSQL.
