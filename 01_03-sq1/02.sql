DROP TABLE IF EXISTS Relationships;

DROP TABLE IF EXISTS Items;

DROP TABLE IF EXISTS Tasks;

DROP TABLE IF EXISTS Dwarves;

DROP TABLE IF EXISTS Squads;

CREATE TABLE Squads (
    squad_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    leader_id INTEGER REFERENCES Dwarves(dwarf_id)
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
    assigned_to INTEGER REFERENCES Dwarves(dwarf_id),
    STATUS TEXT NOT NULL
);

CREATE TABLE Items (
    item_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    owner_id INTEGER REFERENCES Dwarves(dwarf_id)
);

CREATE TABLE Relationships (
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves(dwarf_id),
    related_to INTEGER NOT NULL REFERENCES Dwarves(dwarf_id),
    relationship TEXT NOT NULL,
    PRIMARY KEY (dwarf_id, related_to)
);

-- Squads and Dwarves reference each other (leader_id <-> squad_id).
-- Insert Dwarves with squad_id=NULL first, insert Squads, then update squad_id.
INSERT INTO
    Dwarves (dwarf_id, name, age, profession)
VALUES
    (1, 'Urist McAxe', 45, 'miner'),
    (2, 'Doren Bronzehead', 32, 'carpenter'),
    (3, 'Morul Stonepick', 28, 'miner'),
    (4, 'Sibrek Hammerman', 67, 'warrior'),
    (5, 'Etur Craftstone', 51, 'blacksmith'),
    (6, 'Zulban Geargrind', 38, 'miner'),
    (7, 'Medtob Ironwill', 22, 'farmer'),
    (8, 'Kadol Swiftpick', 55, 'miner'),
    (9, 'Tun Stonecarver', 19, 'carpenter'),
    (10, 'Vucar Deepmine', 44, 'warrior'),
    (11, 'Voldimr Putler', 151, 'warrior');

INSERT INTO
    Squads
VALUES
    (1, 'Iron Hammers', 1),  -- Urist leads
    (2, 'Stone Carvers', 4),  -- Sibrek leads
    (3, 'Ghost Patrol', 8),  -- Kadol leads but is unassigned (no squad_id)
    (4, 'Liberaxi', NULL),  -- no leader
    (5, 'Guardians', 11);

-- squad with no leader
UPDATE
    Dwarves
SET
    squad_id = 1
WHERE
    dwarf_id IN (1, 2, 10);

UPDATE
    Dwarves
SET
    squad_id = 2
WHERE
    dwarf_id IN (4, 5, 9);

UPDATE
    Dwarves
SET
    squad_id = 5
WHERE
    dwarf_id IN (11);

-- dwarves 3, 6, 7, 8 remain squad_id = NULL
INSERT INTO
    Tasks
VALUES
    (1, 'Mine iron in sector 7', 1, 'in_progress'),
    (2, 'Construct north wall', 2, 'pending'),
    (3, 'Forge iron bars', 5, 'pending'),
    (4, 'Guard the gate', 4, 'completed'),
    (5, 'Harvest crops', 7, 'pending'),
    (6, 'Repair armor', NULL, 'pending'),
    (7, 'Scout the caves', 3, 'in_progress'),
    (8, 'Build furniture', 2, 'completed'),
    (9, 'Sharpen weapons', 6, 'pending'),
    (10, 'Brew ale', NULL, 'pending'),
    (11, 'Chill', 11, 'pending');

-- weapon owners: 1(45), 4(67), 3(28)  avg = 46.67
-- armor owners:  2(32), 4(67), 7(22)  avg = 40.33
-- tool owners:   1(45), 5(51), NULL   avg = 48.0
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

INSERT INTO
    Relationships
VALUES
    (1, 2, 'Друг'),
    (2, 1, 'Друг'),
    (4, 5, 'Друг'),
    (5, 4, 'Друг'),
    (1, 6, 'Друг'),
    (6, 1, 'Друг'),
    (7, 3, 'Супруг'),
    (3, 7, 'Супруг'),
    (8, 7, 'Супруг'),  -- why not?..
    (2, 9, 'Родитель'),
    (1, 3, 'Родитель');

-- 1
SELECT
    s.*
FROM
    Squads AS s
WHERE
    s.leader_id IS NULL;

-- 2
SELECT
    d.*
FROM
    Dwarves AS d
WHERE
    d.age > 150
    AND LOWER(d.profession) = LOWER('Warrior');

-- 3
SELECT
    DISTINCT d.*
FROM
    Dwarves AS d
    INNER JOIN Items AS i ON i.owner_id = d.dwarf_id
WHERE
    i.type = 'weapon';

-- 4
SELECT
    d.dwarf_id,
    t.status,
    count(t.assigned_to)
FROM
    Dwarves AS d
    LEFT JOIN Tasks AS t ON t.assigned_to = d.dwarf_id
GROUP BY
    d.dwarf_id,
    t.status;

-- 7
SELECT
    *
FROM
    Squads AS s
WHERE
    s.name = 'Guardians';

-- 5
SELECT
    t.description
FROM
    Dwarves AS d
    LEFT JOIN Tasks AS t ON t.assigned_to = d.dwarf_id
    LEFT JOIN Squads AS s ON s.squad_id = d.squad_id
WHERE
    s.name = 'Guardians'
GROUP BY
    t.description;

-- 6
SELECT
    d1.name AS related_from,
    d2.name AS related_to,
    r.relationship
FROM
    Relationships AS r
    INNER JOIN Dwarves AS d1 ON d1.dwarf_id = r.dwarf_id
    INNER JOIN Dwarves AS d2 ON d2.dwarf_id = r.related_to;
