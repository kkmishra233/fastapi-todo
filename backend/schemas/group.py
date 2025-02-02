from pydantic import BaseModel

class GroupCreate(BaseModel):
    name: str

class GroupUpdate(BaseModel):
    name: str

class GroupOut(GroupCreate):
    id: int

    class Config:
        orm_mode = True