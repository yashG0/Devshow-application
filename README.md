# DevShow API 🚀

[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Live](https://img.shields.io/badge/Live-devshow.yashgaurkar.me-8A2BE2?style=flat)](https://devshow.yashgaurkar.me)

FastAPI backend for **DevShow**, a platform where developers build, publish, and share their project portfolios. It handles accounts, profiles, projects, screenshot uploads, and the public pages the frontend renders, and it runs independently from the React frontend.

| | |
|---|---|
| **Live app** | [devshow.yashgaurkar.me](https://devshow.yashgaurkar.me) |
| **Frontend repo** | [github.com/yashG0/DevShow](https://github.com/yashG0/DevShow) (React + TypeScript) |
| **Backend repo** | [github.com/yashG0/DevShow-backend](https://github.com/yashG0/DevShow-backend) (this repository) |

---

## ⚡ Key Highlights

- **Server-side authorization:** JWT bearer authentication with Argon2 password hashing. Ownership is checked before any project is modified, and the public API never exposes unpublished projects.
- **Migration-managed schema:** PostgreSQL through SQLAlchemy, with every schema change versioned in Alembic.
- **Image pipeline:** Pillow validates uploads (JPEG, PNG, WEBP, up to 5 MB), converts them to WebP, and generates thumbnails, with up to 5 ordered screenshots per project.
- **Public portfolio API:** Unauthenticated endpoints for developer profiles and published projects, with a view counter.
- **Validated at the boundary:** Pydantic schemas validate every request before it reaches the service and database layer.
- **Deployed:** API on an Azure Ubuntu VM with HTTPS on a custom domain, frontend on Vercel.

---

## 🏛️ System Architecture

<p align="center">
  <img src="assets/architecture/arch.png" alt="DevShow API architecture: React frontend on Vercel, reverse proxy and FastAPI on an Azure VM, PostgreSQL, local media storage" width="100%" />
</p>

### Request Flow

1. **Ingress:** The reverse proxy terminates HTTPS and forwards the request to Uvicorn. CORS allows only the configured origins.
2. **Validation:** Pydantic schemas validate the request body and parameters at the API boundary.
3. **Authentication:** For private routes, an auth dependency verifies the JWT bearer token and loads the current user.
4. **Authorization & Logic:** The router and service layer check project ownership, then read or write through SQLAlchemy.
5. **Media:** Uploaded images are validated and converted to WebP with Pillow and saved under `uploads/`. Metadata (path, alt text, position) is stored with the project in PostgreSQL.

---

## 🗄️ Data Model

```text
User
 └── Project
      └── ProjectMedia
```

| Entity | Stores |
| :----- | :----- |
| **User** | Email, username, display name, biography, avatar path, GitHub / LinkedIn / website URLs, password hash |
| **Project** | Title, slug, tagline, Markdown description, technologies, repository URL, demo URL, publication state, view count, timestamps |
| **ProjectMedia** | Parent project, uploaded file path, alternative text, display position |

Alembic manages schema changes:

```bash
# apply migrations
uv run alembic upgrade head

# create a migration after model changes
uv run alembic revision --autogenerate -m "describe change"
```

Review generated migrations before applying them.

---

## 📁 Project Structure

```text
DevShow-backend/
├── app/
│   ├── main.py
│   ├── models/          # user, project, project_media
│   ├── schemas/         # auth, user, project (Pydantic)
│   ├── routers/         # auth, users, projects, public
│   ├── services/        # project business logic
│   └── dependencies/    # auth dependencies
├── migrations/          # Alembic
│   ├── versions/
│   └── env.py
├── uploads/
│   └── projects/
├── alembic.ini
├── pyproject.toml
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL, or [Podman](https://podman.io/) / Docker to run it locally

### Local Development

1. **Clone and install:**

   ```bash
   git clone git@github.com:yashG0/DevShow-backend.git
   cd DevShow-backend
   uv sync
   ```

2. **Configure the environment.** Create a `.env` file (never commit it):

   ```env
   DATABASE_URL=postgresql+psycopg://devshow:devshow@localhost:5432/devshow
   JWT_SECRET=replace-with-a-strong-secret
   ```

3. **Start PostgreSQL:**

   ```bash
   podman run -d \
     --name devshow-postgres \
     -e POSTGRES_DB=devshow \
     -e POSTGRES_USER=devshow \
     -e POSTGRES_PASSWORD=devshow \
     -p 5432:5432 \
     postgres:16
   ```

4. **Run migrations and start the API:**

   ```bash
   uv run alembic upgrade head
   uv run uvicorn app.main:app --reload
   ```

| URL | Purpose |
| :-- | :------ |
| `http://localhost:8000` | API |
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |

---

## 📖 API Reference

The OpenAPI specification at `/docs` is the authoritative reference for request and response schemas.

### Endpoints

| Method | Endpoint | Auth | Description |
| :----- | :------- | :--- | :---------- |
| `GET` | `/health` | — | Health check |
| `POST` | `/api/auth/register` | — | Create an account |
| `POST` | `/api/auth/token` | — | Log in (form data), returns a bearer token |
| `GET` | `/api/auth/me` | Bearer | Current user |
| `GET` | `/api/me` | Bearer | Get your developer profile |
| `PATCH` | `/api/me` | Bearer | Update your developer profile |
| `POST` | `/api/projects` | Bearer | Create a project |
| `GET` | `/api/projects` | Bearer | List your projects |
| `GET` | `/api/projects/{project_id}` | Bearer | Get a project |
| `PATCH` | `/api/projects/{project_id}` | Bearer | Update a project |
| `DELETE` | `/api/projects/{project_id}` | Bearer | Delete a project |
| `PATCH` | `/api/projects/{project_id}/publish` | Bearer | Publish or unpublish a project |
| `POST` | `/api/projects/{project_id}/media` | Bearer | Upload a screenshot |
| `DELETE` | `/api/projects/{project_id}/media/{media_id}` | Bearer | Delete a screenshot |
| `GET` | `/api/public/dev/{username}` | — | Public developer profile |
| `GET` | `/api/public/dev/{username}/{slug}` | — | Public project page (increments the view counter) |

### Authentication

Login accepts form data (`username` is the account email):

```bash
curl -X POST http://localhost:8000/api/auth/token \
  -d "username=you@example.com" \
  -d "password=your-password"
```

Use the returned token on private routes:

```bash
curl http://localhost:8000/api/me \
  -H "Authorization: Bearer <token>"
```

Public routes need no token:

```bash
curl http://localhost:8000/api/public/dev/<username>
```

Access tokens expire after **7 days**. Logout is stateless: the frontend discards its stored token.

### Media Constraints

| Constraint | Value |
| :--------- | :---- |
| Screenshots per project | 5 |
| Maximum file size | 5 MB |
| Accepted formats | JPEG, PNG, WEBP |
| Stored output | WEBP |

Processed images are served from `/uploads/...`.

---

## 🛡️ Security

- Passwords are hashed with Argon2
- JWT authentication protects private resources
- Project ownership is checked before modification
- Unpublished projects are hidden from public endpoints
- Uploaded images are validated before processing
- CORS origins are explicitly configured: `http://localhost:5173` and `http://127.0.0.1:5173` for development, `https://devshow.yashgaurkar.me` for production
- Secrets come from environment variables, and database credentials are not stored in source code

Authorization is enforced by the backend even when the frontend hides protected functionality.

---

## 📦 Production Deployment

| Component | Where it runs |
| :-------- | :------------ |
| Frontend | Vercel, at [devshow.yashgaurkar.me](https://devshow.yashgaurkar.me) |
| API | Azure Ubuntu VM, Uvicorn behind a reverse proxy with HTTPS |
| Database | PostgreSQL |
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

## ⚠️ Known Limitations

- **View counter is not deduplicated.** Every public project request increments it, so refreshes and bots inflate the count.
- **Stateless JWT with no revocation.** Tokens last 7 days, there are no refresh tokens, and logout only discards the token on the client.
- **Media lives on the VM's local disk.** It is tied to a single machine and is not shared across instances.
- **No automated tests yet.** Endpoints are verified manually through Swagger UI.
- **No email verification, password reset, or OAuth.**
- **Single-instance deployment.**

---

## 🔮 Next Steps

- Automated tests for auth, ownership checks, and publishing, run in CI
- Deduplicated view counting
- Refresh tokens
- Object storage for media

---

## 📄 License

License information will be added before the project is distributed for external use.

---

## 👨‍💻 Author

**Yash Gaurkar** · MCA Student · Backend Developer

- GitHub: [github.com/yashG0](https://github.com/yashG0)
- LinkedIn: [linkedin.com/in/yash-gaurkar-a897b3228](https://linkedin.com/in/yash-gaurkar-a897b3228)
- Portfolio: [portfolio.yashgaurkar.me](https://portfolio.yashgaurkar.me)