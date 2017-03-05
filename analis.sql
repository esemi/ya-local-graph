SELECT from_id, a1.name as from_label, to_id, a2.name as to_label FROM "similar"
JOIN "artist" a1 ON (from_id = a1.id)
JOIN "artist" a2 ON (to_id = a2.id)
LIMIT 100