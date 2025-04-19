from tortoise.queryset import QuerySet
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserOut

async def get_all_users(skip: int = 0, limit: int = 100) -> QuerySet[User]:
    return await User.all().offset(skip).limit(limit)

async def get_user_by_id(id: int) -> User:
    return await User.get_or_none(id=id)

async def get_or_create_user(data: UserCreate) -> User:
    user, created = await User.get_or_create(**data.dict(exclude_unset=True))
    return user, created

async def update_user(id: int, data: UserUpdate) -> User:
    record = await get_user_by_id(id)
    if record:
        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)
        await record.save()
    return record

async def delete_user(id: int) -> None:
    db_todo = await get_user_by_id(id)
    if db_todo:
        await db_todo.delete()
        return True
    return False