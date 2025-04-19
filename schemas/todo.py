from datetime import datetime
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str | None = None

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class TodoResponse(TodoCreate):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
