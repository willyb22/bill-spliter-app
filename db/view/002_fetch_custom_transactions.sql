WITH trans_description AS (
    SELECT t.id, t.timestamp, d.detail AS "description"
    FROM transactions t
        JOIN descriptions d
        ON t.description = d.id
), trans_detail AS (
    SELECT t.timestamp, t.description, td.participant_id, td.amount
    FROM trans_description t
        JOIN transaction_detail td
        ON t.id = td.transaction_id
)
SELECT t.timestamp, p.name, t.description, t.amount
FROM trans_detail t
    JOIN participant p
    ON t.participant_id = p.id
ORDER BY t.timestamp ASC