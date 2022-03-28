from peewee import SqliteDatabase, Model

from Core.utils.dot_env import DotEnv

database = SqliteDatabase(r'D:\4-PROJELER\Python\PALA_BOT\database.db')


class BaseModel(Model):
    class Meta:
        database = database
