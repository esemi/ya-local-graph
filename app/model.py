# -*- coding: utf-8 -*-

from peewee import PostgresqlDatabase, Model, CharField, IntegerField, IntegrityError, BooleanField, CompositeKey

from app.config import DB_USER, DB_PSWD, DB_NAME

db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PSWD, autorollback=True)
db.connect()


class Artist(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    is_main_node = BooleanField(index=True)
    need_crawl_similar = BooleanField(index=True)

    class Meta:
        database = db


class Similar(Model):
    from_id = IntegerField()
    to_id = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('from_id', 'to_id')


def get_artists_for_similar():
    return Artist.select().where(Artist.need_crawl_similar == True)


def save_new_artist(id, name, is_similar=False):
    try:
        Artist.create(id=id, name=name, is_main_node=not is_similar,
                      need_crawl_similar=not is_similar)
        return True
    except IntegrityError:
        return False


def save_new_similar_edge(from_id, to_id):
    try:
        Similar.create(from_id=from_id, to_id=to_id)
        return True
    except IntegrityError:
        return False


def update_need_crawl_similar(id, state):
    q = Artist.update(need_crawl_similar=state).where(Artist.id == id)
    q.execute()

