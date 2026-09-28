from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.project_media import router as project_media_router
from app.api.projects import router as projects_router
from app.api.public import router as public_router
from app.api.users import router as users_router

app = FastAPI(
    title="DevShow API",
    description="Backend API for DevShow",
    version="0.1.0",
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(project_media_router)
app.include_router(public_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
