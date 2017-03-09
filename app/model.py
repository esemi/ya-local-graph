# -*- coding: utf-8 -*-

from peewee import PostgresqlDatabase, Model, CharField, IntegerField, IntegrityError, BooleanField, CompositeKey, \
    RawQuery

from app.config import DB_USER, DB_PSWD, DB_NAME, GRAPH_EXPORT_LIMIT

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


class Genre(Model):
    id = IntegerField(primary_key=True)
    genre = CharField(unique=True)

    class Meta:
        database = db


class ArtistGenre(Model):
    artist_id = IntegerField()
    genre_id = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('artist_id', 'genre_id')
        db_table = 'artist_genre'


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


def add_genre(name):
    return Genre.get_or_create(genre=name)[0].id


def get_genres():
    res = Genre.select()
    return {g.genre: g.id for g in res}


def update_artist_genres(artist_id, genres_id):
    ArtistGenre.delete().where(ArtistGenre.artist_id == artist_id).execute()
    for g in genres_id:
        ArtistGenre.create(artist_id=artist_id, genre_id=g)


def fetch_graph_short():
    """Return genre graph w/o single nodes"""
    rq = RawQuery(Similar, 'SELECT from_id, a1.name as from_label, to_id, a2.name as to_label '
                           'FROM "similar" '
                           'JOIN "artist" a1 ON (from_id = a1.id) '
                           'JOIN "artist" a2 ON (to_id = a2.id) '
                           'WHERE a1.is_main_node = True AND a2.is_main_node = True LIMIT %d' % GRAPH_EXPORT_LIMIT)
    nodes = {}
    edges = []
    for obj in rq.execute():
        nodes[obj.from_id] = {'label': obj.from_label, 'color': 'red'}
        nodes[obj.to_id] = {'label': obj.to_label, 'color': 'red'}
        edges.append((obj.from_id, obj.to_id))
    return nodes, edges


def fetch_graph_full():
    """Return full graph w/o single nodes"""
    rq = RawQuery(Similar, 'SELECT from_id, a1.name as from_label, to_id, a2.name as to_label, '
                           'a1.is_main_node as from_main, a2.is_main_node as to_main '
                           'FROM "similar" '
                           'JOIN "artist" a1 ON (from_id = a1.id) '
                           'JOIN "artist" a2 ON (to_id = a2.id) '
                           'LIMIT %d' % GRAPH_EXPORT_LIMIT)
    nodes = {}
    edges = []
    for obj in rq.execute():
        nodes[obj.from_id] = {'label': obj.from_label, 'color': 'red' if obj.from_main else 'blue'}
        nodes[obj.to_id] = {'label': obj.to_label, 'color': 'red' if obj.to_main else 'blue'}
        edges.append((obj.from_id, obj.to_id))
    return nodes, edges


def update_degree():
    rq = RawQuery(Similar, 'UPDATE "artist" SET '
                           'degree_output = (SELECT COUNT(*) FROM "similar" WHERE from_id = id), '
                           'degree_input = (SELECT COUNT(*) FROM "similar" WHERE to_id = id)')
    rq.execute()
