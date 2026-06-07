# AI Document Assistant

## Overview

AI Document Assistant is a production-style backend application that enables users to upload PDF documents and interact with them using natural language questions.

The system implements a Retrieval-Augmented Generation (RAG) pipeline by extracting text from uploaded PDFs, splitting content into chunks, retrieving relevant context, and generating AI-powered answers using Google's Gemini model.

The project was built using FastAPI, PostgreSQL, SQLAlchemy, JWT Authentication, Docker, and Pytest.

---

## Features

### Authentication & Security

* User Registration
* User Login
* JWT-based Authentication
* Protected Routes
* Password Hashing using bcrypt

### Document Management

* Upload PDF Documents
* Store Document Metadata
* View Uploaded Documents
* Retrieve Document Details
* Delete Documents
* User-specific Document Ownership

### AI-Powered Question Answering

* PDF Text Extraction using PyMuPDF
* Text Chunking Pipeline
* Chunk Storage in PostgreSQL
* Retrieval-Augmented Generation (RAG)
* Gemini AI Integration
* Context-Aware Question Answering

### Chat Management

* Save Question History
* Save AI Responses
* Retrieve Previous Conversations

### Testing & Deployment

* Automated API Testing with Pytest
* Dedicated Test Database
* Dockerized Application
* Docker Compose Setup

---

## Tech Stack

### Backend

* FastAPI
* Python

### Database

* PostgreSQL
* SQLAlchemy ORM

### Authentication

* JWT
* Passlib (bcrypt)

### AI & Document Processing

* Google Gemini API
* PyMuPDF

### Testing

* Pytest
* FastAPI TestClient

### Deployment

* Docker
* Docker Compose

---

## Architecture

User Uploads PDF

↓

Text Extraction

↓

Text Chunking

↓

Store Chunks in PostgreSQL

↓

User Asks Question

↓

Retrieve Relevant Chunks

↓

Gemini AI

↓

Generate Answer

↓

Store Chat History

---

## Project Structure

```text
AI_document_assistant/
│
├── app/
│   ├── routes/
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── retrieval.py
│   ├── chunking.py
│   ├── pdf_utils.py
│   ├── gemini_service.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_documents.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## API Endpoints

### Authentication

| Method | Endpoint       |
| ------ | -------------- |
| POST   | /auth/register |
| POST   | /auth/login    |
| GET    | /auth/me       |

### Documents

| Method | Endpoint          |
| ------ | ----------------- |
| POST   | /documents/upload |
| GET    | /documents        |
| GET    | /documents/{id}   |
| DELETE | /documents/{id}   |

### AI Features

| Method | Endpoint                     |
| ------ | ---------------------------- |
| POST   | /documents/{id}/search       |
| POST   | /documents/{id}/ask          |
| GET    | /documents/{id}/chat-history |

---

## Running Locally

```bash
git clone <repository_url>

cd AI_document_assistant

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Running with Docker

```bash
docker compose up --build
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Testing

Run all tests:

```bash
pytest
```

Current test coverage includes:

* Authentication
* Login
* Registration
* JWT Authorization
* Document Operations

---

## Future Improvements

* Vector Database Integration
* Semantic Search using Embeddings
* Role-Based Access Control
* Multi-document Conversations
* Cloud Storage Support
* CI/CD Pipeline
* Production Deployment

---

## Key Learnings

This project demonstrates:

* Backend API Development
* Authentication & Authorization
* Database Design
* ORM Relationships
* PDF Processing
* Retrieval-Augmented Generation (RAG)
* AI Integration
* Automated Testing
* Containerization with Docker
* Production-Oriented Backend Architecture
