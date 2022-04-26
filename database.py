from peewee import *

db = SqliteDatabase('d.db')  # connection to db


class BaseClass(Model):  # base class
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class AnekdotBezMata(BaseClass):
    text = CharField()

    class Meta:
        db_table = 'anekdots_bezmata'


class AnekdotMat(BaseClass):
    text = CharField()

    class Meta:
        db_table = 'anekdots_smatom'


class Likes(BaseClass):
    likes_id = TextField()

    class Meta:
        db_table = 'likes'


class User(BaseClass):
    likes = ForeignKeyField(Likes)
    cnt_anekdots_smatom = IntegerField()
    cnt_anekdots_bezmata = IntegerField()
    cnt_likes_smatom = IntegerField()
    cnt_likes_bezmata = IntegerField()
    user_id = IntegerField()
    page_smatom = IntegerField()
    page_bezmata = IntegerField()

    class Meta:
        db_table = 'users'


with db:
    db.create_tables([AnekdotMat, AnekdotBezMata, Likes, User])
