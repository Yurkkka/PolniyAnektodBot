from peewee import *

db = SqliteDatabase('database.db')  # connection to db


class BaseClass(Model):  # base class
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Anekdot(BaseClass):
    text = CharField()

    class Meta:
        db_table = 'anekdots'


class User(BaseClass):
    user_id = IntegerField()

    class Meta:
        db_table = 'users'


with db:
    db.create_tables([Anekdot, User])

print('done')
