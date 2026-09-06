from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth_routes, endpoints

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fintech AI Agent API", description="Financial Research AI Agent Backend")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(endpoints.router, prefix="/api", tags=["Endpoints"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Fintech AI Agent API"}
