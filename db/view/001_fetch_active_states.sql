WITH active_state AS (
    SELECT s.id, s.participant_id, s.participant_to, s.amount
    FROM states s 
        JOIN participant p
        ON s.participant_id = p.id
    WHERE p.is_active=1
)
SELECT a.id, a.participant_id, a.participant_to, a.amount
FROM active_state a
    JOIN participant p
    ON a.participant_to = p.id
WHERE p.is_active=1
ORDER BY a.participant_id ASC, a.participant_to ASC;
