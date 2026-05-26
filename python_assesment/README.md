# Tech Stack

Python 3.11+
FastAPI
MongoDB
Redis
Docker Compose
Motor (Async MongoDB Driver)
redis.asyncio
Pytest + HTTPX


# API Endpoints

---

## Submit Document

## Endpoint


POST /documents

## Request

json
{
  "user_id": "user1",
  "title": "AI Research",
  "content": "Long document content"
}

## Response

json
{
  "document_id": "6651f2b4f8a8d1f2f3a4b5c6",
  "status": "queued"
}

## Status Codes

201 Created
429 Too Many Requests
422 Validation Error

## Get Document Status

## Endpoint


GET /documents/{document_id}

## Response

{
  "document_id": "6651f2b4f8a8d1f2f3a4b5c6",
  "status": "completed",
  "summary": "Summary text..."
}

## Status Codes

200 OK
400 Invalid ObjectId
404 Not Found


## List User Documents

### Endpoint

GET /users/{user_id}/documents

## Query Parameters

page = page number
page_size = Results per page
status = Optional status filter

## Example


GET /users/user1/documents?page=1&page_size=10&status=completed


## Health Check

## Endpoint


GET /health

## Response

json
{
  "mongo": "healthy",
  "redis": "healthy"
}

# Data Model

## Document Schema


{
  "_id": ObjectId,
  "user_id": "user1",
  "title": "Document Title",
  "content": "Raw content",
  "content_hash": "sha256 hash",
  "status": "queued",
  "summary": null,
  "created_at": "datetime",
  "updated_at": "datetime"
}

---

# MongoDB Indexes

we are creating indexes at application startup.

## Compound Index

("user_id", 1),
("status", 1)


## Content Hash Index


"content_hash"

Optimizes duplicate content detection and cache lookups.

## Rate Limiting

Each user can have a maximum of:

3 active jobs

where active jobs include:

queued or processing

Redis is used to atomically track active job counts. When exceeded: 429 Too Many Requests is returned.

## Worker Design

The worker continuously polls the Redis queue and processes documents asynchronously.

Processing flow:

queued -> processing -> completed / failed

## Race Condition Handling

To prevent multiple workers processing the same document:

find_one_and_update(
    {
        "_id": id,
        "status": "queued"
    }
)

using this, only one worker can claim the job.

# Error Handling for:-

ObjectId validation
structured exception logging
worker failure handling
HTTP error responses


# Logging for:-

API requests
worker processing
failures
app startup


## Run Using Docker Compose

docker compose up --build


# Access Application

http://localhost:8000


# Running Tests

pytest -v

## Sample API Requests

## Submit Document


POST http://localhost:8000/documents \
 "Content-Type: application/json" \
 {
  "user_id": "user1",
  "title": "Test",
  "content": "This is a test document"
}

---

## Get Document Status


curl http://localhost:8000/documents/{document_id}

## List User Documents


"http://localhost:8000/users/user1/documents?page=1&page_size=10"

# Tests:-

document submission tests
validation tests
rate limiting tests
cache tests
worker processing tests
pagination tests
health endpoint tests
error handling tests