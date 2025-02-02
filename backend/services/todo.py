from tortoise.queryset import QuerySet
from models.todo import Todo
from schemas.todo import TodoCreate, TodoUpdate

async def get_all_todos(skip: int = 0, limit: int = 100) -> QuerySet[Todo]:
    return await Todo.all().offset(skip).limit(limit)

async def get_todo_by_id(todo_id: int) -> Todo:
    return await Todo.get_or_none(id=todo_id)

async def create_todo(todo_data: TodoCreate) -> Todo:
    db_todo = await Todo.create(**todo_data.dict())
    return db_todo

async def update_todo(todo_id: int, todo_data: TodoUpdate) -> Todo:
    db_todo = await get_todo_by_id(todo_id)
    if db_todo:
        update_data = todo_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        await db_todo.save()
    return db_todo

async def delete_todo(todo_id: int) -> None:
    db_todo = await get_todo_by_id(todo_id)
    if db_todo:
        await db_todo.delete()
        return True
    return False