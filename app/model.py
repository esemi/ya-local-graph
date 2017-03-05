# -*- coding: utf-8 -*-

from peewee import PostgresqlDatabase, Model, CharField, IntegerField, IntegrityError, BooleanField, CompositeKey, \
    RawQuery

from app.config import DB_USER, DB_PSWD, DB_NAME

db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PSWD, autorollback=True)
db.connect()


class Artist(Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    is_main_node = BooleanField(index=True)
    need_crawl_similar = BooleanField(index=True)
    degree_input = IntegerField()
    degree_output = IntegerField()

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


def fetch_graph_genre_short():
    """Return main genre graph w/o single nodes"""
    rq = RawQuery(Similar, 'SELECT from_id, a1.name as from_label, to_id, a2.name as to_label '
                           'FROM "similar" '
                           'JOIN "artist" a1 ON (from_id = a1.id) '
                           'JOIN "artist" a2 ON (to_id = a2.id) '
                           'WHERE a1.is_main_node = True AND a2.is_main_node = True')
    nodes = {}
    edges = []
    for obj in rq.execute():
        nodes[obj.from_id] = obj.from_label
        nodes[obj.to_id] = obj.to_label
        edges.append((obj.from_id, obj.to_id))
    return nodes, edges
