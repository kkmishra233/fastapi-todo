from tortoise.queryset import QuerySet
from models.group import Group 
from schemas.group import GroupCreate

async def get_all_groups(skip: int = 0, limit: int = 100) -> QuerySet[Group]:
    return await Group.all().offset(skip).limit(limit)

async def get_group_by_id(id: int) -> Group:
    return await Group.get_or_none(id=id)

async def get_or_create_group(data: GroupCreate) -> Group:
    group, created = await Group.get_or_create(**data.dict())
    return group, created

async def delete_group(id: int) -> bool:
    record = await get_group_by_id(id)
    if record:
        await record.delete()
        return True
    return False