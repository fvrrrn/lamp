-- 1
SELECT
    d.*,
    s.*
FROM
    Dwarves d
    INNER JOIN Squads s ON s.squad_id = d.squad_id;

-- 2
SELECT
    d.*
FROM
    Dwarves d
WHERE
    d.squad_id IS NULL
    AND d.profession = 'miner';

-- 3
SELECT
    t.*
FROM
    Tasks t
WHERE
    t.priority = (
        SELECT
            MAX(priority)
        FROM
            Tasks
    )
    AND t.status = 'pending';

-- 4
SELECT
    d.dwarf_id,
    COUNT(*) AS count
FROM
    Dwarves d
    INNER JOIN Items i ON i.owner_id = d.dwarf_id
GROUP BY
    d.dwarf_id;

-- 5
SELECT
    s.squad_id,
    COUNT(d.dwarf_id) AS count
FROM
    Squads s
    LEFT JOIN Dwarves d ON d.squad_id = s.squad_id
GROUP BY
    s.squad_id;

-- 6
SELECT
    d.profession,
    COUNT(*) AS count
FROM
    Tasks AS t
    INNER JOIN Dwarves AS d ON d.dwarf_id = t.assigned_to
WHERE
    t.status IN ('pending', 'in_progress')
GROUP BY
    d.profession
ORDER BY
    count DESC;

-- 7
SELECT
    i.type,
    avg(d.age) AS average_age
FROM
    Items AS i
    LEFT JOIN Dwarves AS d ON d.dwarf_id = i.owner_id
GROUP BY
    i.type;

-- 8
SELECT
    d.*
FROM
    Dwarves AS d
    LEFT JOIN items AS i ON i.owner_id = d.dwarf_id
WHERE
    i.item_id IS NULL
    AND d.age > (
        SELECT
            avg(age)
        FROM
            Dwarves
    );
