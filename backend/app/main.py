from fastapi import FastAPI
# This file initializes the FastAPI application, sets up CORS middleware, and includes the API router for task management.
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import tasks

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application with metadata for documentation
app = FastAPI(
    title="Task Management API",
    description="A simple API for managing tasks with user authentication and permissions.",
    version="1.0.0"
)
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}
# Configure CORS middleware to allow requests from the frontend URL specified in the settings.
# This is necessary for the frontend to communicate with the backend API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL], 
    allow_credentials=True,# Allow cookies and authentication headers to be included in requests
    allow_methods=["*"],# Allow all HTTP methods (GET, POST, PUT, DELETE, etc.) to be used in requests
    allow_headers=["*"],# Allow all headers to be included in requests, which is necessary for authentication and other custom headers.
)

# Include the API router for task management
# which defines the endpoints for creating, reading, updating, and deleting tasks.
app.include_router(tasks.router)
