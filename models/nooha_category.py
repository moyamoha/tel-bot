from tortoise.models import Model
from tortoise import fields


class NoohaCategory(Model):
    id = fields.IntField(primary_key=True)
    nooha = fields.ForeignKeyField('models.Nooha', on_delete=fields.CASCADE)
    category = fields.ForeignKeyField('models.Category', on_delete=fields.CASCADE)

    class Meta:
        table = "nooha_category"