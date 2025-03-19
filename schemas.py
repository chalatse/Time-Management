from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime

class TaskUpdate(BaseModel):
    status: str
