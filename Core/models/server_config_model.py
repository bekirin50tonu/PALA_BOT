from peewee import *

from Core.models.base_model import BaseModel


class ServerConfig(BaseModel):
    server_id = BigIntegerField()
    prefix = CharField(max_length=3)
    message_channel_id = BigIntegerField()
    bot_channel_id = BigIntegerField(null=True)
    all_time = BooleanField(default=False)
    music_volume = FloatField(default=20)
