from peewee import PostgresqlDatabase, Model, CharField, ForeignKeyField
import os

db = PostgresqlDatabase(
    os.getenv('DB_NAME', 'IoTDevices'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASS', 'dbpass'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=5432
)


class BaseModel(Model):
    class Meta:
        database = db


class APIUser(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()


class Location(BaseModel):
    name = CharField(unique=True)


class Device(BaseModel):
    name = CharField()
    type = CharField()
    login = CharField(unique=True)
    password = CharField()
    location = ForeignKeyField(Location, backref='devices')
    api_user = ForeignKeyField(APIUser, backref='devices')


def create_tables():
    with db:
        db.create_tables([APIUser, Location, Device])


if __name__ == '__main__':
    create_tables()
