CREATE TABLE "artist" (
  "id" integer NOT NULL,
  "name" character varying NOT NULL
);
ALTER TABLE "artist" ADD CONSTRAINT "artist_id" PRIMARY KEY ("id");
ALTER TABLE "artist" ADD "need_similar" boolean NOT NULL DEFAULT '0';
CREATE INDEX "artist_need_similar" ON "artist" ("need_similar");

ALTER TABLE "artist"
ALTER "need_similar" TYPE boolean,
ALTER "need_similar" SET DEFAULT 'false',
ALTER "need_similar" SET NOT NULL,
ADD "need_crawl_similar" boolean NOT NULL DEFAULT 'false';
ALTER TABLE "artist" RENAME "need_similar" TO "is_main_node";

DROP INDEX "artist_need_similar";
CREATE INDEX "artist_is_main_node_need_crawl_similar" ON "artist" ("is_main_node", "need_crawl_similar");

UPDATE artist SET need_crawl_similar = True WHERE is_main_node = True;

CREATE TABLE "similar" (
  "from_id" integer NOT NULL,
  "to_id" integer NOT NULL
);
ALTER TABLE "similar" ADD CONSTRAINT "similar_from_to" PRIMARY KEY ("from_id", "to_id");
ALTER TABLE "similar" ADD FOREIGN KEY ("from_id") REFERENCES "artist" ("id") ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE "similar" ADD FOREIGN KEY ("to_id") REFERENCES "artist" ("id") ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "artist" ADD "degree" integer NOT NULL DEFAULT '0';
ALTER TABLE "artist"
ALTER "degree" TYPE integer,
ALTER "degree" SET DEFAULT '0',
ALTER "degree" SET NOT NULL,
ADD "degree_output" integer NOT NULL DEFAULT '0';
ALTER TABLE "artist" RENAME "degree" TO "degree_input";


CREATE TABLE "genre" (
  "id" serial NOT NULL,
  "genre" character varying NOT NULL
);