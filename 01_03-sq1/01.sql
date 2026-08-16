DROP TABLE IF EXISTS Items;

DROP TABLE IF EXISTS Tasks;

DROP TABLE IF EXISTS Dwarves;

DROP TABLE IF EXISTS Squads;

CREATE TABLE Squads (
    squad_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    mission TEXT NOT NULL
);

CREATE TABLE Dwarves (
    dwarf_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    profession TEXT NOT NULL,
    squad_id INTEGER REFERENCES Squads(squad_id)
);

CREATE TABLE Tasks (
    task_id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    priority INTEGER NOT NULL,
    assigned_to INTEGER REFERENCES Dwarves(dwarf_id),
    STATUS TEXT NOT NULL
);

CREATE TABLE Items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    owner_id INTEGER REFERENCES Dwarves(dwarf_id)
);

INSERT INTO
    Squads
VALUES
    (1, 'Iron Hammers', 'Mine iron ore'),
    (2, 'Stone Carvers', 'Build walls'),
    (3, 'Ghost Patrol', 'Guard entrance');

INSERT INTO
    Dwarves
VALUES
    (1, 'Urist McAxe', 45, 'miner', 1),
    (2, 'Doren Bronzehead', 32, 'carpenter', 1),
    (3, 'Morul Stonepick', 28, 'miner', NULL),
    (4, 'Sibrek Hammerman', 67, 'warrior', 2),
    (5, 'Etur Craftstone', 51, 'blacksmith', 2),
    (6, 'Zulban Geargrind', 38, 'miner', NULL),
    (7, 'Medtob Ironwill', 22, 'farmer', NULL),
    (8, 'Kadol Swiftpick', 55, 'miner', NULL),
    (9, 'Tun Stonecarver', 19, 'carpenter', 2),
    (10, 'Vucar Deepmine', 44, 'warrior', 1);

INSERT INTO
    Tasks
VALUES
    (
        1,
        'Mine iron in sector 7',
        3,
        1,
        'in_progress'
    ),
    (
        2,
        'Construct north wall',
        2,
        2,
        'pending'
    ),
    (
        3,
        'Forge iron bars',
        3,
        5,
        'pending'
    ),
    (
        4,
        'Guard the gate',
        1,
        4,
        'completed'
    ),
    (
        5,
        'Harvest crops',
        2,
        7,
        'pending'
    ),
    (
        6,
        'Repair armor',
        3,
        NULL,
        'pending'
    ),
    (
        7,
        'Scout the caves',
        2,
        3,
        'in_progress'
    ),
    (
        8,
        'Build furniture',
        1,
        2,
        'completed'
    ),
    (
        9,
        'Sharpen weapons',
        3,
        6,
        'pending'
    ),
    (
        10,
        'Brew ale',
        2,
        NULL,
        'pending'
    );

INSERT INTO
    Items
VALUES
    (1, 'Iron Pickaxe', 'tool', 1),
    (2, 'Steel Axe', 'weapon', 1),
    (3, 'Leather Armor', 'armor', 2),
    (4, 'Bronze Hammer', 'weapon', 4),
    (5, 'Iron Shield', 'armor', 4),
    (6, 'Copper Tongs', 'tool', 5),
    (7, 'Silver Amulet', 'armor', 7),
    (8, 'Community Anvil', 'tool', NULL),
    (9, 'Iron Sword', 'weapon', 3);

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
