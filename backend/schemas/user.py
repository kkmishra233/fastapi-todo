from typing import List
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class UserUpdate(BaseModel):
    username: str

class UserOut(UserCreate):
    id: int

    class Config:
        orm_mode = True