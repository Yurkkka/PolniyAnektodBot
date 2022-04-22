from peewee import *

db = SqliteDatabase('dbmy.db')  # connection to db


class BaseClass(Model):  # base class
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Anekdot(BaseClass):
    text = TextField()

    class Meta:
        db_table = 'anekdots'


class Likes(BaseClass):
    likes_id = TextField()

    class Meta:
        db_table = 'likes'


class User(BaseClass):
    likes = ForeignKeyField(Likes)
    cnt_anekdots = IntegerField()
    cnt_likes = IntegerField()
    user_id = IntegerField()
    page = IntegerField()

    class Meta:
        db_table = 'users'


with db:
    db.create_tables([Anekdot, Likes, User])
