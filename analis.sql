SELECT from_id, a1.name as from_label, to_id, a2.name as to_label FROM "similar"
JOIN "artist" a1 ON (from_id = a1.id)
JOIN "artist" a2 ON (to_id = a2.id)
WHERE a1.is_main_node = True AND a2.is_main_node = True
LIMIT 100

SELECT COUNT(*)
FROM "artist"
WHERE ("degree_input" > '0' OR degree_output > 0) AND "is_main_node" = '1'
LIMIT 50

SELECT from_id, a1.name as from_label, to_id, a2.name as to_label FROM "similar"
JOIN "artist" a1 ON (from_id = a1.id)
JOIN "artist" a2 ON (to_id = a2.id)
WHERE a1.is_main_node = True AND a2.is_main_node = True