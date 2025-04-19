from inspect import getmembers
from fastapi import FastAPI
from tortoise.contrib.starlette import register_tortoise
from core.config import settings

def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)

def init_db(app: FastAPI):
    """
    Init database models.
    :param app:
    :return:
    """
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        generate_schemas=True,
        modules={"models": ["models.todo","models.user","models.group"]},
    )


def init_routers(app: FastAPI):
    """
    Initialize routers defined in `app.api`
    :param app:
    :return:
    """
    from routers import todo, health
    app.include_router(todo.router)
    app.include_router(health.router)