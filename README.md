# DevShow API

> Production-oriented backend API for DevShow — a modern platform for developers to build, manage, publish, and showcase their projects.

DevShow API powers developer profiles, project management, project media, authentication, publishing, and public portfolio pages.

It is built as a standalone FastAPI service and is designed to run independently from the React frontend.

---

## ✨ What is DevShow?

DevShow is a developer showcase platform focused on one simple goal:

**Give developers a polished place to present what they build.**

The backend provides the application services behind:

- Developer accounts
- Developer profiles
- Project management
- Project publishing
- Project screenshots
- Public developer profiles
- Public project pages
- Project view counting

The frontend is maintained separately.

---

## 🚀 Core Features

### Authentication

- User registration
- Email-based login
- JWT bearer authentication
- Argon2 password hashing
- Protected API routes
- Seven-day access token expiry
- Stateless authentication

### Developer Profiles

Developers can manage:

- Username
- Display name
- Biography
- Avatar path
- GitHub URL
- LinkedIn URL
- Personal website

### Projects

Authenticated developers can:

- Create projects
- Update projects
- Delete projects
- Publish projects
- Unpublish projects
- Add technology tags
- Add GitHub repository links
- Add live demo links
- Write Markdown project descriptions

### Project Media

Projects support:

- Up to 5 screenshots
- JPEG, PNG, and WEBP uploads
- 5 MB maximum upload size
- Image validation using Pillow
- Image processing and WebP output
- Thumbnail resizing
- Ordered media positions
- Media deletion

### Public API

Published content is available without authentication.

Public developer profile:

```text
GET /api/public/dev/{username}
```

Public project:

```text
GET /api/public/dev/{username}/{slug}
```

Public project requests also increment the project's view counter.

---

## 🧱 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend language |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| PostgreSQL | Relational database |
| Alembic | Database migrations |
| Pydantic | Validation and schemas |
| Pydantic Settings | Environment configuration |
| Argon2 | Password hashing |
| PyJWT | JWT authentication |
| Pillow | Image processing |
| psycopg | PostgreSQL driver |
| Uvicorn | ASGI server |
| Podman | Local container infrastructure |

---

## 🏗️ Architecture

The DevShow backend follows a modular FastAPI architecture.

```text
                    ┌──────────────────────┐
                    │   React Frontend     │
                    │   DevShow Web App    │
                    └──────────┬───────────┘
                               │
                         HTTPS / JSON
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    │                      │
                    │  Auth                │
                    │  Profiles            │
                    │  Projects            │
                    │  Media               │
                    │  Public API          │
                    └──────────┬───────────┘
                               │
                         SQLAlchemy
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    └──────────────────────┘
```

The API is intentionally separated from the frontend so that the backend can be deployed independently.

---

## 📁 Project Structure

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── project.py
│   │   └── project_media.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── project.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── projects.py
│   │   └── public.py
│   │
│   ├── services/
│   │   └── project.py
│   │
│   └── dependencies/
│       └── auth.py
│
├── migrations/
│   ├── versions/
│   └── env.py
│
├── uploads/
│   └── projects/
│
├── .env
├── alembic.ini
├── pyproject.toml
└── README.md
```

> Directory names may evolve as the project grows. The architecture is organized around API routes, validation schemas, database models, services, and infrastructure.

---

## 🔐 Authentication

DevShow uses stateless JWT bearer authentication.

### Login

```http
POST /api/auth/token
```

The login endpoint accepts form data:

```text
username=<email>
password=<password>
```

A successful login returns an access token.

Authenticated requests use:

```http
Authorization: Bearer <token>
```

### Password Security

Passwords are never stored directly.

DevShow uses **Argon2** for password hashing.

### Token Lifetime

Access tokens currently expire after:

```text
7 days
```

Logout is stateless: the frontend discards its stored access token.

---

## 🗄️ Database

DevShow uses PostgreSQL with SQLAlchemy.

Current core entities:

```text
User
 │
 └── Project
      │
      └── ProjectMedia
```

### User

Stores developer identity and profile information.

### Project

Stores:

- Title
- Slug
- Tagline
- Markdown description
- Technologies
- Repository URL
- Demo URL
- Publication state
- View count
- Timestamps

### ProjectMedia

Stores:

- Project relationship
- Uploaded file path
- Alternative text
- Display position

---

## 🔄 Database Migrations

Alembic manages schema changes.

Run migrations with:

```bash
uv run alembic upgrade head
```

Create a new migration after model changes:

```bash
uv run alembic revision --autogenerate -m "describe change"
```

Review generated migrations before applying them.

---

## ⚙️ Local Development

### Prerequisites

Recommended:

- Python 3.14+
- uv
- PostgreSQL
- Podman

### Clone

```bash
git clone git@github.com:yashG0/DevShow-backend.git
cd DevShow-backend
```

### Install dependencies

```bash
uv sync
```

### Environment

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://devshow:devshow@localhost:5432/devshow
JWT_SECRET=replace-with-a-strong-secret
```

Never commit real production secrets.

### Start PostgreSQL

For local development, PostgreSQL can run through Podman:

```bash
podman run -d \
  --name devshow-postgres \
  -e POSTGRES_DB=devshow \
  -e POSTGRES_USER=devshow \
  -e POSTGRES_PASSWORD=devshow \
  -p 5432:5432 \
  postgres:16
```

### Run migrations

```bash
uv run alembic upgrade head
```

### Start the API

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

Alternative OpenAPI documentation:

```text
http://localhost:8000/redoc
```

---

## ❤️ Health Check

The service exposes:

```http
GET /health
```

Example:

```json
{
  "status": "ok"
}
```

This endpoint is useful for local checks, reverse proxies, containers, and deployment health monitoring.

---

## 🔌 API Overview

### Authentication

```text
POST /api/auth/register
POST /api/auth/token
GET  /api/auth/me
```

### Developer Profile

```text
GET   /api/me
PATCH /api/me
```

### Projects

```text
POST   /api/projects
GET    /api/projects
GET    /api/projects/{project_id}
PATCH  /api/projects/{project_id}
DELETE /api/projects/{project_id}

PATCH /api/projects/{project_id}/publish
```

### Project Media

```text
POST   /api/projects/{project_id}/media
DELETE /api/projects/{project_id}/media/{media_id}
```

### Public

```text
GET /api/public/dev/{username}
GET /api/public/dev/{username}/{slug}
```

The OpenAPI specification available at `/docs` is the authoritative reference for request and response schemas.

---

## 🖼️ Media Handling

Uploaded project screenshots are processed by the backend.

Current constraints:

```text
Maximum screenshots per project: 5
Maximum file size:               5 MB
Accepted formats:                JPEG / PNG / WEBP
Stored output:                   WEBP
```

Images are validated and processed with Pillow.

Uploaded media is served through:

```text
/uploads/...
```

---

## 🌐 CORS

Development origins include:

```text
http://localhost:5173
http://127.0.0.1:5173
```

The production frontend origin is:

```text
https://devshow.yashgaurkar.me
```

Production CORS configuration should be kept explicit rather than allowing arbitrary origins.

---

## 🛡️ Security

The backend follows several security principles:

- Passwords are hashed with Argon2
- JWT authentication protects private resources
- Project ownership is checked before modification
- Unpublished projects are hidden from public endpoints
- Uploaded images are validated before processing
- Production secrets are provided through environment variables
- CORS origins are explicitly configured
- Database credentials are not stored in source code

The backend remains responsible for authorization even when the frontend hides protected functionality.

---

## 🧪 API Development

FastAPI automatically generates an OpenAPI specification.

During development:

```text
Swagger UI
http://localhost:8000/docs
```

and:

```text
ReDoc
http://localhost:8000/redoc
```

These interfaces can be used to inspect and manually test API endpoints.

---

## 📦 Production Deployment

The planned production architecture is:

```text
                         Internet
                            │
                            ▼
              https://devshow.yashgaurkar.me
                            │
                         Vercel
                       React Frontend
                            │
                            │ HTTPS
                            ▼
                 https://api.yashgaurkar.me
                            │
                            ▼
                         Nginx
                            │
                            ▼
                     FastAPI / Uvicorn
                            │
                            ▼
                       PostgreSQL
```

The frontend and backend are deployed independently.

Production deployment will use:

- Linux server
- FastAPI
- Uvicorn
- Nginx
- PostgreSQL
- HTTPS
- Environment-based configuration

Deployment-specific instructions will be added as the infrastructure is finalized.

---

## 📊 Current Project Status

DevShow API currently includes:

- [x] User registration
- [x] JWT login
- [x] Password hashing
- [x] Developer profile API
- [x] Project CRUD
- [x] Project publishing
- [x] Project media uploads
- [x] Project media deletion
- [x] Public developer API
- [x] Public project API
- [x] Project view counter
- [x] PostgreSQL integration
- [x] Alembic migrations
- [x] CORS configuration
- [x] Static media serving
- [x] Health endpoint

---

## 🧭 Product Scope

DevShow deliberately keeps the first version focused.

The backend does **not** currently attempt to provide:

- Social feeds
- Likes
- Bookmarks
- Follows
- Developer discovery
- Search
- GitHub importing
- OAuth
- Refresh tokens
- Email verification
- Password reset
- Comments
- Analytics dashboards
- Redis-based infrastructure
- Object storage integration

These can be evaluated independently as the product evolves.

---

## 🧠 Engineering Principles

DevShow follows a few practical principles:

### Keep the architecture understandable

Prefer straightforward FastAPI modules and explicit API boundaries.

### Validate at the API boundary

Pydantic schemas handle request validation before data reaches the service/database layer.

### Keep authorization server-side

The frontend is never treated as a security boundary.

### Ship incrementally

Each meaningful feature is implemented, verified, and committed independently.

### Avoid premature infrastructure

The initial system uses PostgreSQL and local media storage without introducing unnecessary distributed infrastructure.

---

## 🤝 Contributing

DevShow is currently maintained as a personal product project.

Contribution guidelines will be added if the repository becomes open for external contributions.

---

## 📄 License

License information will be added before the project is distributed for external use.

---

## 👨‍💻 Author

**Yash Gaurkar**

MCA Student · Backend Developer

Built with:

```text
Python
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Podman
Linux
```
