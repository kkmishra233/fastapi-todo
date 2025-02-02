from fastapi import APIRouter, HTTPException
from schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from services.todo import (
    create_todo, get_all_todos, get_todo_by_id, update_todo, delete_todo
)

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=TodoResponse)
async def create_todo_handler(todo: TodoCreate):
    todo_obj = await create_todo(todo)
    return todo_obj

@router.get("/", response_model=list[TodoResponse])
async def get_todos_handler():
    return await get_all_todos()

@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo_handler(todo_id: int):
    todo = await get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo_handler(todo_id: int, todo_data: TodoUpdate):
    todo = await update_todo(todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.delete("/{todo_id}")
async def delete_todo_handler(todo_id: int):
    status = await delete_todo(todo_id)
    if not status:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
