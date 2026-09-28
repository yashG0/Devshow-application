from fastapi import FastAPI

app = FastAPI(
    title="DevShow API",
    description="Backend API for DevShow",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
