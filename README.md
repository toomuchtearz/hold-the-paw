# Hold The Paw - Backend API Documentation

Welcome to the backend repository for the Hold The Paw platform. This API is built with Django REST Framework.

## 📚 Interactive API Documentation (Swagger / ReDoc)

You do not need to guess the endpoints or payload structures! We use auto-generated, interactive documentation. Once the server is running locally (usually on `http://127.0.0.1:8001`), visit one of the following links:

* **Swagger UI (Best for testing):** `/api/v1/schema/swagger-ui/`
* **ReDoc (Best for reading):** `/api/v1/schema/redoc/`
* **Raw OpenAPI Schema:** `/api/v1/schema/`

From the Swagger UI, you can directly execute API calls and see the exact JSON responses.

## 🔐 Authentication Flow (JWT)

This API uses JSON Web Tokens (JWT) for authentication. Most endpoints in the `pets/`, `conversations/`, and `users/` routes require a valid access token.

**1. Login / Obtain Tokens**
* **Endpoint:** `POST /api/v1/token/`
* **Payload:** `{"email": "your_email", "password": "your_password"}`
* **Response:** Returns an `access` token (short lifespan) and a `refresh` token (longer lifespan).

**2. Authenticating Requests**
For protected endpoints, include the access token in the HTTP Headers of your request:
`Authorization: Bearer <your_access_token>`

**3. Refreshing the Access Token**
When the `access` token expires, use the `refresh` token to get a new one without forcing the user to log in again.
* **Endpoint:** `POST /api/v1/token/refresh/`
* **Payload:** `{"refresh": "<your_refresh_token>"}`

## 🧭 Core API Routes Overview

All endpoints are currently on version 1 (`/api/v1/`). Check the Swagger UI for specific query parameters, pagination rules, and JSON payloads.

* **`/api/v1/users/`** - User registration, profile management, and password updates.
* **`/api/v1/pets/`** - Browsing, filtering, and creating pet adoption listings.
* **`/api/v1/conversations/`** - Managing private messaging between adopters and pet listers. 
  * *Note to Frontend:* Messages for a specific conversation are accessed via the nested action: `GET/POST /api/v1/conversations/{id}/messages/`.