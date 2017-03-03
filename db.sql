CREATE TABLE "artist" (
  "id" integer NOT NULL,
  "name" character varying NOT NULL
);

ALTER TABLE "artist" ADD CONSTRAINT "artist_id" PRIMARY KEY ("id");