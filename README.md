# DevShow API

> FastAPI backend for DevShow — a platform where developers build, manage, publish, and share their project portfolios.

DevShow API powers developer profiles, project management, project media, authentication, publishing, and public portfolio pages. It is a standalone service that runs independently from the React frontend.

| | |
|---|---|
| **Live app** | [devshow.yashgaurkar.me](https://devshow.yashgaurkar.me) |
| **Frontend repo** | [github.com/yashG0/DevShow](https://github.com/yashG0/DevShow) (React + TypeScript) |
| **Backend repo** | [github.com/yashG0/DevShow-backend](https://github.com/yashG0/DevShow-backend) (this repository) |

---

## ✨ What is DevShow?

DevShow is a developer showcase platform with one goal:

**Give developers a polished place to present what they build.**

The backend provides the services behind:

- Developer accounts and profiles
- Project management and publishing
- Project screenshots
- Public developer profiles and project pages
- Project view counting

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

- Create, update, and delete projects
- Publish and unpublish projects
- Add technology tags
- Add GitHub repository and live demo links
- Write Markdown project descriptions

### Project Media

- Up to 5 screenshots per project
- JPEG, PNG, and WEBP uploads, 5 MB maximum
- Image validation and processing with Pillow
- WebP output with thumbnail resizing
- Ordered media positions
- Media deletion

### Public API

Published content is available without authentication.

```text
GET /api/public/dev/{username}
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
| Pydantic / Pydantic Settings | Validation, schemas, environment configuration |
| Argon2 | Password hashing |
| PyJWT | JWT authentication |
| Pillow | Image validation and processing |
| psycopg | PostgreSQL driver |
| Uvicorn | ASGI server |
| Podman | Local container infrastructure |
| uv | Dependency management |

---

## 🏗️ Architecture

```text
 Browser
    │
    ▼
 https://devshow.yashgaurkar.me        React frontend (Vercel)
    │
    │  HTTPS / JSON + JWT bearer token
    ▼
 Reverse proxy (HTTPS)                  Azure Ubuntu VM
    │
    ▼
 FastAPI / Uvicorn
    │   Auth · Profiles · Projects · Media · Public API
    │
    ├── SQLAlchemy ──▶ PostgreSQL
    └── Pillow ──────▶ uploads/ (local disk)
```

The frontend and API are deployed independently. The API validates every request at the boundary with Pydantic, enforces ownership server-side, and persists data through SQLAlchemy.

---

## 📁 Project Structure

```text
backend/
├── app/
│   ├── main.py
│   ├── models/          # user, project, project_media
│   ├── schemas/         # auth, user, project (Pydantic)
│   ├── routers/         # auth, users, projects, public
│   ├── services/        # project business logic
│   └── dependencies/    # auth dependencies
│
├── migrations/          # Alembic
│   ├── versions/
│   └── env.py
│
├── uploads/
│   └── projects/
│
├── alembic.ini
├── pyproject.toml
└── README.md
```

> Directory names may evolve as the project grows.

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

A successful login returns an access token. Authenticated requests use:

```http
Authorization: Bearer <token>
```

### Password Security

Passwords are never stored directly. DevShow uses **Argon2** for password hashing.

### Token Lifetime

Access tokens expire after **7 days**. Logout is stateless: the frontend discards its stored token. See [Known Limitations](#-known-limitations).

---

## 🗄️ Database

PostgreSQL with SQLAlchemy.

```text
User
 └── Project
      └── ProjectMedia
```

- **User** — developer identity and profile information
- **Project** — title, slug, tagline, Markdown description, technologies, repository URL, demo URL, publication state, view count, timestamps
- **ProjectMedia** — project relationship, uploaded file path, alternative text, display position

### Migrations

Alembic manages schema changes.

```bash
# apply migrations
uv run alembic upgrade head

# create a migration after model changes
uv run alembic revision --autogenerate -m "describe change"
```

Review generated migrations before applying them.

---

## ⚙️ Local Development

### Prerequisites

- Python 3.14+
- uv
- PostgreSQL (or Podman, below)

### Setup

```bash
git clone git@github.com:yashG0/DevShow-backend.git
cd DevShow-backend
uv sync
```

Create a `.env` file (never commit it):

```env
DATABASE_URL=postgresql+psycopg://devshow:devshow@localhost:5432/devshow
JWT_SECRET=replace-with-a-strong-secret
```

Start PostgreSQL with Podman:

```bash
podman run -d \
  --name devshow-postgres \
  -e POSTGRES_DB=devshow \
  -e POSTGRES_USER=devshow \
  -e POSTGRES_PASSWORD=devshow \
  -p 5432:5432 \
  postgres:16
```

Run migrations and start the API:

```bash
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

| URL | Purpose |
|---|---|
| `http://localhost:8000` | API |
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |

---

## ❤️ Health Check

```http
GET /health
```

```json
{ "status": "ok" }
```

Useful for local checks, reverse proxies, and deployment monitoring.

---

## 🔌 API Overview

```text
# Authentication
POST /api/auth/register
POST /api/auth/token
GET  /api/auth/me

# Developer profile
GET   /api/me
PATCH /api/me

# Projects
POST   /api/projects
GET    /api/projects
GET    /api/projects/{project_id}
PATCH  /api/projects/{project_id}
DELETE /api/projects/{project_id}
PATCH  /api/projects/{project_id}/publish

# Project media
POST   /api/projects/{project_id}/media
DELETE /api/projects/{project_id}/media/{media_id}

# Public (no authentication)
GET /api/public/dev/{username}
GET /api/public/dev/{username}/{slug}
```

The OpenAPI specification at `/docs` is the authoritative reference for request and response schemas.

---

## 🖼️ Media Handling

```text
Maximum screenshots per project: 5
Maximum file size:               5 MB
Accepted formats:                JPEG / PNG / WEBP
Stored output:                   WEBP
```

Uploads are validated and processed with Pillow, then served from `/uploads/...`.

---

## 🌐 CORS

Development origins:

```text
http://localhost:5173
http://127.0.0.1:5173
```

Production origin:

```text
https://devshow.yashgaurkar.me
```

Production CORS is explicit; arbitrary origins are not allowed.

---

## 🛡️ Security

- Passwords are hashed with Argon2
- JWT authentication protects private resources
- Project ownership is checked before modification
- Unpublished projects are hidden from public endpoints
- Uploaded images are validated before processing
- Production secrets come from environment variables
- CORS origins are explicitly configured
- Database credentials are not stored in source code

Authorization is enforced by the backend even when the frontend hides protected functionality.

---

## 📦 Production Deployment

DevShow is deployed with the frontend and API hosted separately.

| Component | Where it runs |
|---|---|
| Frontend | Vercel — [devshow.yashgaurkar.me](https://devshow.yashgaurkar.me) |
| API | Azure Ubuntu VM, Uvicorn behind `<reverse proxy: Caddy / Nginx>` with HTTPS |
| Process manager | `<e.g. systemd service name>` |
| Database | PostgreSQL — `<how it runs, e.g. Podman container on the VM>` |
| Media | Local disk under `uploads/` on the VM |

Deploying a new version:

```bash
git pull
uv sync
uv run alembic upgrade head
# restart the API service
```

Production configuration is supplied through environment variables (`DATABASE_URL`, `JWT_SECRET`).

---

## 📊 Current Project Status

- [x] User registration and JWT login
- [x] Argon2 password hashing
- [x] Developer profile API
- [x] Project CRUD and publishing
- [x] Project media uploads and deletion
- [x] Public developer and project APIs
- [x] Project view counter
- [x] PostgreSQL integration and Alembic migrations
- [x] CORS configuration
- [x] Static media serving
- [x] Health endpoint
- [x] Deployed on Azure VM with HTTPS
- [ ] Automated test suite
- [ ] CI pipeline

---

## ⚠️ Known Limitations

- **View counter is not deduplicated.** Every public project request increments it, so refreshes and bots inflate the count.
- **Stateless JWT with no revocation.** Tokens last 7 days, there are no refresh tokens, and logout only discards the token on the client.
- **Media lives on the VM's local disk.** It is tied to a single machine and is not shared across instances.
- **No automated tests yet.** Endpoints are verified manually through Swagger UI.
- **No email verification or password reset.**
- **Single-instance deployment.**

---

## 🧭 Product Scope

DevShow deliberately keeps the first version focused. The backend does **not** currently provide:

- Social feeds, likes, bookmarks, follows, or comments
- Developer discovery or search
- GitHub importing or OAuth
- Refresh tokens, email verification, or password reset
- Analytics dashboards
- Redis-based infrastructure or object storage

These can be evaluated independently as the product evolves.

---

## 🔮 Next Steps

- Automated tests for auth, ownership checks, and publishing, run in CI
- Deduplicated view counting
- Refresh tokens
- Object storage for media

---

## 🧠 Engineering Principles

- **Keep the architecture understandable** — straightforward FastAPI modules and explicit API boundaries.
- **Validate at the API boundary** — Pydantic schemas validate requests before data reaches the service and database layer.
- **Keep authorization server-side** — the frontend is never treated as a security boundary.
- **Ship incrementally** — each meaningful feature is implemented, verified, and committed independently.
- **Avoid premature infrastructure** — PostgreSQL and local media storage, without unnecessary distributed systems.

---

## 🤝 Contributing

DevShow is currently maintained as a personal product project. Contribution guidelines will be added if the repository becomes open for external contributions.

---

## 📄 License

License information will be added before the project is distributed for external use.

---

## 👨‍💻 Author

**Yash Gaurkar** — MCA Student · Backend Developer

- GitHub: [github.com/yashG0](https://github.com/yashG0)
- LinkedIn: [linkedin.com/in/yash-gaurkar-a897b3228](https://linkedin.com/in/yash-gaurkar-a897b3228)
- Portfolio: [portfolio.yashgaurkar.me](https://portfolio.yashgaurkar.me)
