from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ALLOWED_ORIGINS
from app.routers import health, procedures, intake, validation, rag

app = FastAPI(
    title="AI Procedure Copilot API",
    description="Backend API for AI-guided public service procedures",
    version="1.0.0"
)

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
