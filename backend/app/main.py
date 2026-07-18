from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS
from app.routers import health, procedures, intake, validation, rag

app = FastAPI(
    title="AI Procedure Copilot API",
    description="Backend API for AI-guided public service procedures",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "AI Procedure Copilot API",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
        "rag_search_get": "/v1/rag/search?query=giay%20chung%20sinh&procedure_id=dang-ky-khai-sinh&top_k=3",
        "rag_search_post": "/v1/rag/search",
    }

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(procedures.router)
app.include_router(intake.router)
app.include_router(validation.router)
app.include_router(rag.router)
