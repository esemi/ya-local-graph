--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: artist; Type: TABLE; Schema: public; Owner: ya; Tablespace: 
--

CREATE TABLE artist (
    id integer NOT NULL,
    name character varying NOT NULL,
    similar_crawled boolean DEFAULT false NOT NULL,
    need_crawl_similar boolean DEFAULT false NOT NULL,
    degree_input integer DEFAULT 0 NOT NULL,
    degree_output integer DEFAULT 0 NOT NULL,
    is_primary boolean DEFAULT false NOT NULL
);


ALTER TABLE public.artist OWNER TO ya;

--
-- Name: artist_genre; Type: TABLE; Schema: public; Owner: ya; Tablespace: 
--

CREATE TABLE artist_genre (
    artist_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.artist_genre OWNER TO ya;

--
-- Name: genre; Type: TABLE; Schema: public; Owner: ya; Tablespace: 
--

CREATE TABLE genre (
    id integer NOT NULL,
    genre character varying NOT NULL
);


ALTER TABLE public.genre OWNER TO ya;

--
-- Name: genre_id_seq; Type: SEQUENCE; Schema: public; Owner: ya
--

CREATE SEQUENCE genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genre_id_seq OWNER TO ya;

--
-- Name: genre_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ya
--

ALTER SEQUENCE genre_id_seq OWNED BY genre.id;


--
-- Name: similar; Type: TABLE; Schema: public; Owner: ya; Tablespace: 
--

CREATE TABLE "similar" (
    from_id integer NOT NULL,
    to_id integer NOT NULL,
    "position" smallint DEFAULT 0::smallint NOT NULL
);


ALTER TABLE public."similar" OWNER TO ya;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: ya
--

ALTER TABLE ONLY genre ALTER COLUMN id SET DEFAULT nextval('genre_id_seq'::regclass);


--
-- Name: ArtistGenre_artist_id_genre_id; Type: CONSTRAINT; Schema: public; Owner: ya; Tablespace: 
--

ALTER TABLE ONLY artist_genre
    ADD CONSTRAINT "ArtistGenre_artist_id_genre_id" PRIMARY KEY (artist_id, genre_id);


--
-- Name: artist_id; Type: CONSTRAINT; Schema: public; Owner: ya; Tablespace: 
--

ALTER TABLE ONLY artist
    ADD CONSTRAINT artist_id PRIMARY KEY (id);


--
-- Name: genre_genre; Type: CONSTRAINT; Schema: public; Owner: ya; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT genre_genre UNIQUE (genre);


--
-- Name: genre_id; Type: CONSTRAINT; Schema: public; Owner: ya; Tablespace: 
--

ALTER TABLE ONLY genre
    ADD CONSTRAINT genre_id PRIMARY KEY (id);


--
-- Name: similar_from_to; Type: CONSTRAINT; Schema: public; Owner: ya; Tablespace: 
--

ALTER TABLE ONLY "similar"
    ADD CONSTRAINT similar_from_to PRIMARY KEY (from_id, to_id);


--
-- Name: artist_is_main_node_need_crawl_similar; Type: INDEX; Schema: public; Owner: ya; Tablespace: 
--

CREATE INDEX artist_is_main_node_need_crawl_similar ON artist USING btree (similar_crawled, need_crawl_similar);


--
-- Name: artist_is_primary; Type: INDEX; Schema: public; Owner: ya; Tablespace: 
--

CREATE INDEX artist_is_primary ON artist USING btree (is_primary);

CREATE INDEX "similar_position" ON "similar" ("position");

--
-- Name: ArtistGenre_artist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ya
--

ALTER TABLE ONLY artist_genre
    ADD CONSTRAINT "ArtistGenre_artist_id_fkey" FOREIGN KEY (artist_id) REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ArtistGenre_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ya
--

ALTER TABLE ONLY artist_genre
    ADD CONSTRAINT "ArtistGenre_genre_id_fkey" FOREIGN KEY (genre_id) REFERENCES genre(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: similar_from_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ya
--

ALTER TABLE ONLY "similar"
    ADD CONSTRAINT similar_from_id_fkey FOREIGN KEY (from_id) REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: similar_to_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ya
--

ALTER TABLE ONLY "similar"
    ADD CONSTRAINT similar_to_id_fkey FOREIGN KEY (to_id) REFERENCES artist(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

