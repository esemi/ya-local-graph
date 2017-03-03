# -*- coding: utf-8 -*-

from peewee import PostgresqlDatabase, Model, CharField, IntegerField, IntegrityError

from app.config import DB_USER, DB_PSWD, DB_NAME

db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PSWD, autorollback=True)
db.connect()


class Artist(Model):
    id = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        database = db


def save_new_artist(id, name):
    try:
        Artist.create(id=id, name=name)
        return True
    except IntegrityError:
        return False

