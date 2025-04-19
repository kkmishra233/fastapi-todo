from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255)
    groups = fields.ManyToManyField(
        'models.Group', related_name='users'
    )

    def __str__(self):
        return self.username
