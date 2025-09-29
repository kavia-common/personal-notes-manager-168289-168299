from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_app_settings
from src.core.lifespan import app_lifespan
from src.routes.notes import router as notes_router

# Initialize FastAPI with OpenAPI metadata aligned with the Ocean Professional theme.
app = FastAPI(
    title="Personal Notes API - Ocean Professional",
    description=(
        "A clean, modern REST API for creating, reading, updating, and deleting personal notes. "
        "Styled by the Ocean Professional theme: blue primary accents (#2563EB) with amber highlights (#F59E0B)."
    ),
    version="1.0.0",
    openapi_tags=[
        {
            "name": "notes",
            "description": "Endpoints for managing personal notes (CRUD).",
        },
        {
            "name": "system",
            "description": "System and operational endpoints.",
        },
    ],
    lifespan=app_lifespan,
)

# CORS configuration
settings = get_app_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["system"],
    summary="Health Check",
    description="Simple health check endpoint to verify the service is reachable.",
)
# PUBLIC_INTERFACE
def health_check() -> dict:
    """Return a simple health status payload."""
    return {"status": "ok", "service": "notes-backend", "theme": "Ocean Professional"}


# PUBLIC_INTERFACE
@app.get(
    "/docs/websocket-info",
    tags=["system"],
    summary="WebSocket Usage Info",
    description=(
        "This project currently does not provide WebSocket endpoints. "
        "If real-time features are needed, add explicit WebSocket handlers here "
        "with operation_id, summary, and tags for API docs."
    ),
)
def websocket_info() -> dict:
    """Provide a project-level usage note about WebSocket endpoints."""
    return {
        "websocket": "not-configured",
        "note": "Add WebSocket endpoints here in the future if needed.",
    }


# Include routers
app.include_router(notes_router, prefix="/api/v1")
