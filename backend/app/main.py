from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.exceptions import NotFoundError, AuthorizationError, ConflictError, DatabaseError

app = FastAPI(
    title="EcoTrack API", 
    version="1.0.0",
    description="Clean Architecture Backend for EcoTrack Campus Waste Management"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Exception Handlers ---
@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": str(exc)})

@app.exception_handler(AuthorizationError)
async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(status_code=403, content={"message": str(exc)})

@app.exception_handler(ConflictError)
async def conflict_exception_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"message": str(exc)})

@app.exception_handler(DatabaseError)
async def database_exception_handler(request: Request, exc: DatabaseError):
    # Do not leak database internals to the client
    return JSONResponse(status_code=500, content={"message": "An internal server error occurred."})

# --- Include API Routes ---
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to EcoTrack API"}
