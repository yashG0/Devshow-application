# DevShow 🗂️

[![Live](https://img.shields.io/badge/Live-devshow.yashgaurkar.me-34D399?style=flat)](https://devshow.yashgaurkar.me)
[![Frontend](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://github.com/yashG0/DevShow-backend)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)

A developer showcase platform. Create a public profile, publish projects with screenshots, tech tags, and source/demo links, and share them at clean URLs.

**Live:** [devshow.yashgaurkar.me](https://devshow.yashgaurkar.me)

<!-- Add a hero screenshot here, e.g. docs/screenshot.png:
<p align="center"><img src="docs/screenshot.png" alt="DevShow public project page" width="100%" /></p>
-->

---

## ⚡ Key Highlights

- **Public Pages:** Developer profiles at `/dev/:username` and project pages at `/dev/:username/:slug`. Only published projects are exposed.
- **Project Workspace:** Create, edit, delete, and publish or unpublish projects, with Markdown descriptions, technology tags, repository and live-demo links, and a view counter.
- **Screenshots:** Up to 5 per project, processed into WebP and shown in a thumbnail gallery with a public viewer.
- **JWT Authentication:** Registration, login, bearer-token requests, and protected routes. The backend enforces ownership on private changes.
- **10 Built-in Themes:** Five light and five dark, persisted locally.
- **Centralized API Layer:** One Axios client attaches the token and normalizes API errors.
- **Responsive & Accessible:** Layouts from desktop to mobile, visible focus states, and reduced-motion support.

---

## 🏛️ Architecture

<p align="center">
  <img src="docs/architecture.svg" alt="DevShow architecture: React frontend, FastAPI routes, JWT and ownership checks, PostgreSQL, and processed project media" width="100%" />
</p>

### Request Flow

1. **Client:** The React app calls the API over HTTPS with JSON. Authenticated requests carry `Authorization: Bearer <token>`.
2. **Validation & Authorization:** FastAPI validates each request, verifies the JWT, and checks ownership before any private change.
3. **Persistence:** SQLAlchemy stores profile and project data in PostgreSQL. Schema changes are managed with Alembic.
4. **Media:** Uploaded screenshots are validated, converted to WebP, and served from the uploads path. Their metadata is stored with the project in PostgreSQL.
5. **Public Reads:** Public profile and project routes return published content only.

---

## 🧱 Tech Stack

| Layer | Technologies |
| :---- | :----------- |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS, React Router, Axios, React Markdown |
| **Backend** ([separate repo](https://github.com/yashG0/DevShow-backend)) | FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT, Argon2 |
| **Deployment** | Frontend on Vercel, API on an Azure VM |

---

## 🗺️ Routes

| Route | Access | Purpose |
| :---- | :----- | :------ |
| `/` | Public | Landing page |
| `/login`, `/register` | Public | Authentication |
| `/dev/:username` | Public | Developer profile |
| `/dev/:username/:slug` | Public | Project page |
| `/dashboard` | Authenticated | Developer workspace |
| `/profile` | Authenticated | Profile editor |
| `/projects/new` | Authenticated | Create project |
| `/projects/:projectId` | Authenticated | Project details |
| `/projects/:projectId/edit` | Authenticated | Edit project |

---

## 📁 Project Structure

```text
src/
├── auth/          # AuthProvider and auth types
├── components/    # Navbar, ThemeSwitcher, ProtectedRoute, ui/ primitives
├── layouts/       # AppLayout
├── pages/         # Home, Login, Register, Dashboard, Profile, Project*, Public*
├── services/      # Axios client, error normalization, project API calls
├── theme/         # ThemeProvider and theme definitions
├── App.tsx
└── main.tsx
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js 20+ or [Bun](https://bun.sh) (recommended)
- A running [DevShow backend](https://github.com/yashG0/DevShow-backend)
- Git

### Local Development

1. **Clone the repository:**

   ```bash
   git clone git@github.com:yashG0/DevShow.git
   cd DevShow
   ```

2. **Install dependencies:**

   ```bash
   bun install
   ```

3. **Configure the API** in `.env.local` (defaults to `http://localhost:8000` if omitted):

   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. **Start the dev server:**

   ```bash
   bun run dev
   ```

The app runs on `http://localhost:5173`.

### Production Build

```bash
bun run build
bun run preview   # preview the build locally
```

---

## ⚠️ Known Limitations

- **Token in browser storage.** The access token is persisted in browser storage, so it is exposed to any XSS. The backend's authorization checks, not the frontend's route guards, are what protect data.
- **Client-rendered public pages.** There is no server-side rendering.
- **Frontend checks are UX only.** Validation and authorization are enforced by the backend.

---

## 🔮 Next Steps

- Further accessibility refinement
- Performance optimization
- Production observability

---

## 📄 License

License information will be added.

---

## 👨‍💻 Author

**Yash Gaurkar** · MCA student · Backend developer · [GitHub](https://github.com/yashG0)
