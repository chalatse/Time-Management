from fastapi import FastAPI
from database import engine
import models
from auth import auth_router
from tasks import task_router

# Initialize Database
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI App
app = FastAPI(title="Time Management API")

# Include Routes
app.include_router(auth_router, prefix="/auth")
app.include_router(task_router, prefix="/tasks")

@app.get("/")
def home():
    return {"message": "Welcome to Time Management API"}
