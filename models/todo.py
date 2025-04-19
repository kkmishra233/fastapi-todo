from tortoise.models import Model
from tortoise import fields

class Todo(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    completed = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
