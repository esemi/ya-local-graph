CREATE TABLE artist (
    id integer NOT NULL,
    name character varying NOT NULL,
    similar_crawled boolean DEFAULT false NOT NULL,
    need_crawl_similar boolean DEFAULT false NOT NULL,
    degree_input integer DEFAULT 0 NOT NULL,
    degree_output integer DEFAULT 0 NOT NULL,
    is_primary boolean DEFAULT false NOT NULL
);

CREATE TABLE artist_genre (
    artist_id integer NOT NULL,
    genre_id integer NOT NULL
);

CREATE TABLE genre (
    id integer NOT NULL,
    genre character varying NOT NULL
);


CREATE SEQUENCE genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE genre_id_seq OWNED BY genre.id;

CREATE TABLE "similar" (
    from_id integer NOT NULL,
    to_id integer NOT NULL
);

ALTER TABLE ONLY genre ALTER COLUMN id SET DEFAULT nextval('genre_id_seq'::regclass);

ALTER TABLE ONLY artist_genre
    ADD CONSTRAINT "ArtistGenre_artist_id_genre_id" PRIMARY KEY (artist_id, genre_id);

ALTER TABLE ONLY artist
    ADD CONSTRAINT artist_id PRIMARY KEY (id);

ALTER TABLE ONLY genre
    ADD CONSTRAINT genre_genre UNIQUE (genre);

ALTER TABLE ONLY genre
    ADD CONSTRAINT genre_id PRIMARY KEY (id);

ALTER TABLE ONLY "similar"
    ADD CONSTRAINT similar_from_to PRIMARY KEY (from_id, to_id);


CREATE INDEX artist_is_main_node_need_crawl_similar ON artist USING btree (similar_crawled, need_crawl_similar);
CREATE INDEX artist_is_primary ON artist USING btree (is_primary);

ALTER TABLE ONLY artist_genre
    ADD CONSTRAINT "ArtistGenre_artist_id_fkey" FOREIGN KEY (artist_id) REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY artist_genre
    ADD CONSTRAINT "ArtistGenre_genre_id_fkey" FOREIGN KEY (genre_id) REFERENCES genre(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY "similar"
    ADD CONSTRAINT similar_from_id_fkey FOREIGN KEY (from_id) REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY "similar"
    ADD CONSTRAINT similar_to_id_fkey FOREIGN KEY (to_id) REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE;