from datetime import datetime

from peewee import *

database = SqliteDatabase('storage/reticulum-webchat.db')


class BaseModel(Model):
    class Meta:
        database = database


class LxmfMessage(BaseModel):

    # id = primary key auto increment bigint
    id = BigAutoField()
    hash = CharField(unique=True)  # unique lxmf message hash
    source_hash = CharField(index=True)
    destination_hash = CharField(index=True)
    state = CharField()  # state is converted from internal int to a human friendly string
    progress = FloatField()  # progress is converted from internal float 0.00-1.00 to float between 0.00/100 (2 decimal places)
    is_incoming = BooleanField()  # if true, we should ignore state, it's set to draft by default on incoming messages
    title = TextField()
    content = TextField()
    fields = TextField()  # json string
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # define database and table name
    class Meta:
        table_name = "lxmf_messages"
