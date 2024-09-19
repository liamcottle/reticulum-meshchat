from datetime import datetime, timezone

from peewee import *
from playhouse.migrate import migrate as migrate_database, SqliteMigrator

latest_version = 4  # increment each time new database migrations are added
database = DatabaseProxy()  # use a proxy object, as we will init real db client inside meshchat.py
migrator = SqliteMigrator(database)


# migrates the database
def migrate(current_version):

    # migrate to version 2
    if current_version < 2:
        migrate_database(
            migrator.add_column("lxmf_messages", 'delivery_attempts', LxmfMessage.delivery_attempts),
            migrator.add_column("lxmf_messages", 'next_delivery_attempt_at', LxmfMessage.next_delivery_attempt_at),
        )

    # migrate to version 3
    if current_version < 3:
        migrate_database(
            migrator.add_column("lxmf_messages", 'rssi', LxmfMessage.rssi),
            migrator.add_column("lxmf_messages", 'snr', LxmfMessage.snr),
            migrator.add_column("lxmf_messages", 'quality', LxmfMessage.quality),
        )

    # migrate to version 4
    if current_version < 4:
        migrate_database(
            migrator.add_column("lxmf_messages", 'method', LxmfMessage.method),
        )

    return latest_version


class BaseModel(Model):
    class Meta:
        database = database


class Config(BaseModel):

    id = BigAutoField()
    key = CharField(unique=True)
    value = TextField()
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "config"


class Announce(BaseModel):

    id = BigAutoField()
    destination_hash = CharField(unique=True)  # unique destination hash that was announced
    aspect = TextField(index=True)  # aspect is not included in announce, but we want to filter saved announces by aspect
    identity_hash = CharField(index=True)  # identity hash that announced the destination
    identity_public_key = CharField()  # base64 encoded public key, incase we want to recreate the identity manually
    app_data = TextField(null=True)  # base64 encoded app data bytes

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "announces"


class CustomDestinationDisplayName(BaseModel):

    id = BigAutoField()
    destination_hash = CharField(unique=True)  # unique destination hash
    display_name = CharField()  # custom display name for the destination hash

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "custom_destination_display_names"


class LxmfMessage(BaseModel):

    id = BigAutoField()
    hash = CharField(unique=True)  # unique lxmf message hash
    source_hash = CharField(index=True)
    destination_hash = CharField(index=True)
    state = CharField()  # state is converted from internal int to a human friendly string
    progress = FloatField()  # progress is converted from internal float 0.00-1.00 to float between 0.00/100 (2 decimal places)
    is_incoming = BooleanField()  # if true, we should ignore state, it's set to draft by default on incoming messages
    method = CharField(null=True)  # what method is being used to send the message, e.g: direct, propagated
    delivery_attempts = IntegerField(default=0)  # how many times delivery has been attempted for this message
    next_delivery_attempt_at = FloatField(null=True)  # timestamp of when the message will attempt delivery again
    title = TextField()
    content = TextField()
    fields = TextField()  # json string
    timestamp = FloatField()  # timestamp of when the message was originally created (before ever being sent)
    rssi = IntegerField(null=True)
    snr = FloatField(null=True)
    quality = FloatField(null=True)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "lxmf_messages"


class LxmfConversationReadState(BaseModel):

    id = BigAutoField()
    destination_hash = CharField(unique=True)  # unique destination hash
    last_read_at = DateTimeField()

    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    # define table name
    class Meta:
        table_name = "lxmf_conversation_read_state"
