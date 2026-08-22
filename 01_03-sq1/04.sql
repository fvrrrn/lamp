DROP TABLE IF EXISTS Security_Recommendations;

DROP TABLE IF EXISTS Moon_Phases;

DROP TABLE IF EXISTS Weather_Records;

DROP TABLE IF EXISTS Fortress_Events;

DROP TABLE IF EXISTS Military_Coverage_Zones;

DROP TABLE IF EXISTS Squad_Movement;

DROP TABLE IF EXISTS Military_Stations;

DROP TABLE IF EXISTS Defense_Structures;

DROP TABLE IF EXISTS Expedition_Reports;

DROP TABLE IF EXISTS Expedition_Artifacts;

DROP TABLE IF EXISTS Expedition_Equipment;

DROP TABLE IF EXISTS Expedition_Creatures;

DROP TABLE IF EXISTS Expedition_Sites;

DROP TABLE IF EXISTS Expedition_Members;

DROP TABLE IF EXISTS Expeditions;

DROP TABLE IF EXISTS Creature_Territories;

DROP TABLE IF EXISTS Creature_Attacks;

DROP TABLE IF EXISTS Creature_Sightings;

DROP TABLE IF EXISTS Creatures;

DROP TABLE IF EXISTS Diplomatic_Events;

DROP TABLE IF EXISTS Dwarf_Interests;

DROP TABLE IF EXISTS Trade_Transactions;

DROP TABLE IF EXISTS Caravan_Goods;

DROP TABLE IF EXISTS Traders;

DROP TABLE IF EXISTS Caravans;

DROP TABLE IF EXISTS Orders;

DROP TABLE IF EXISTS Project_Zones;

DROP TABLE IF EXISTS Project_Dependencies;

DROP TABLE IF EXISTS Project_Materials;

DROP TABLE IF EXISTS Project_Workers;

DROP TABLE IF EXISTS Projects;

DROP TABLE IF EXISTS Stockpile_Contents;

DROP TABLE IF EXISTS Fortress_Resources;

DROP TABLE IF EXISTS Extraction_Sites;

DROP TABLE IF EXISTS Workshop_Products;

DROP TABLE IF EXISTS Products;

DROP TABLE IF EXISTS Workshop_Materials;

DROP TABLE IF EXISTS Workshop_Craftsdwarves;

DROP TABLE IF EXISTS Workshops;

DROP TABLE IF EXISTS Squad_Equipment;

DROP TABLE IF EXISTS Squad_Battles;

DROP TABLE IF EXISTS Squad_Training;

DROP TABLE IF EXISTS Squad_Operations;

DROP TABLE IF EXISTS Squad_Members;

DROP TABLE IF EXISTS Military_Squads;

DROP TABLE IF EXISTS Dwarf_Equipment;

DROP TABLE IF EXISTS Equipment;

DROP TABLE IF EXISTS Dwarf_Assignments;

DROP TABLE IF EXISTS Dwarf_Skills;

DROP TABLE IF EXISTS Skills;

DROP TABLE IF EXISTS Dwarves;

DROP TABLE IF EXISTS Locations;

DROP TABLE IF EXISTS Resources;

DROP TABLE IF EXISTS Fortresses;

CREATE TABLE Fortresses (
    fortress_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    founded_year INTEGER NOT NULL,
    depth INTEGER NOT NULL,
    population INTEGER NOT NULL
);

CREATE TABLE Resources (
    resource_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    rarity TEXT NOT NULL,
    description TEXT
);

CREATE TABLE Skills (
    skill_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    skill_type TEXT NOT NULL
);

CREATE TABLE Creatures (
    creature_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    threat_level INTEGER NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    estimated_population INTEGER
);

CREATE TABLE Locations (
    location_id INTEGER PRIMARY KEY,
    zone_id INTEGER,
    name TEXT NOT NULL,
    zone_type TEXT NOT NULL,
    depth INTEGER NOT NULL,
    access_points INTEGER NOT NULL DEFAULT 1,
    fortification_level INTEGER NOT NULL DEFAULT 0,
    wall_integrity INTEGER NOT NULL DEFAULT 100,
    trap_density INTEGER NOT NULL DEFAULT 0,
    choke_points INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE Weather_Records (
    record_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    condition TEXT NOT NULL,
    temperature INTEGER,
    notes TEXT
);

CREATE TABLE Moon_Phases (
    phase_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    phase TEXT NOT NULL,
    illumination INTEGER
);

CREATE TABLE Security_Recommendations (
    recommendation_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    priority INTEGER NOT NULL,
    STATUS TEXT NOT NULL DEFAULT 'open'
);

CREATE TABLE Dwarves (
    dwarf_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    profession TEXT NOT NULL,
    fortress_id INTEGER REFERENCES Fortresses (fortress_id)
);

CREATE TABLE Equipment (
    equipment_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    material_id INTEGER REFERENCES Resources (resource_id),
    quality TEXT NOT NULL
);

CREATE TABLE Extraction_Sites (
    site_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    resource_id INTEGER REFERENCES Resources (resource_id),
    depth INTEGER NOT NULL,
    accessibility TEXT NOT NULL
);

CREATE TABLE Fortress_Resources (
    fortress_id INTEGER NOT NULL REFERENCES Fortresses (fortress_id),
    resource_id INTEGER NOT NULL REFERENCES Resources (resource_id),
    quantity INTEGER NOT NULL DEFAULT 0,
    discovery_date TEXT,
    PRIMARY KEY (fortress_id, resource_id)
);

CREATE TABLE Workshops (
    workshop_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    quality TEXT NOT NULL,
    fortress_id INTEGER REFERENCES Fortresses (fortress_id)
);

CREATE TABLE Stockpile_Contents (
    stockpile_id INTEGER PRIMARY KEY,
    resource_id INTEGER NOT NULL REFERENCES Resources (resource_id),
    quantity INTEGER NOT NULL DEFAULT 0,
    quality TEXT NOT NULL
);

CREATE TABLE Caravans (
    caravan_id INTEGER PRIMARY KEY,
    arrival_date TEXT NOT NULL,
    departure_date TEXT,
    civilization_type TEXT NOT NULL,
    fortress_id INTEGER REFERENCES Fortresses (fortress_id)
);

CREATE TABLE Expeditions (
    expedition_id INTEGER PRIMARY KEY,
    destination TEXT NOT NULL,
    departure_date TEXT NOT NULL,
    return_date TEXT,
    STATUS TEXT NOT NULL
);

CREATE TABLE Fortress_Events (
    event_id INTEGER PRIMARY KEY,
    fortress_id INTEGER NOT NULL REFERENCES Fortresses (fortress_id),
    TYPE TEXT NOT NULL,
    date TEXT NOT NULL,
    description TEXT,
    severity TEXT NOT NULL DEFAULT 'low'
);

CREATE TABLE Defense_Structures (
    structure_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    location_id INTEGER REFERENCES Locations (location_id),
    integrity INTEGER NOT NULL DEFAULT 100,
    construction_date TEXT
);

CREATE TABLE Military_Squads (
    squad_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    formation_type TEXT NOT NULL,
    leader_id INTEGER REFERENCES Dwarves (dwarf_id),
    fortress_id INTEGER REFERENCES Fortresses (fortress_id)
);

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    quality TEXT NOT NULL,
    material_id INTEGER REFERENCES Resources (resource_id),
    value INTEGER NOT NULL DEFAULT 0,
    created_by INTEGER REFERENCES Dwarves (dwarf_id),
    workshop_id INTEGER REFERENCES Workshops (workshop_id)
);

CREATE TABLE Dwarf_Skills (
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    skill_id INTEGER NOT NULL REFERENCES Skills (skill_id),
    LEVEL INTEGER NOT NULL DEFAULT 1,
    experience INTEGER NOT NULL DEFAULT 0,
    date TEXT,
    PRIMARY KEY (dwarf_id, skill_id)
);

CREATE TABLE Dwarf_Assignments (
    assignment_id INTEGER PRIMARY KEY,
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    assignment_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT
);

CREATE TABLE Dwarf_Equipment (
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    equipment_id INTEGER NOT NULL REFERENCES Equipment (equipment_id),
    quality TEXT NOT NULL,
    equipped_date TEXT NOT NULL,
    PRIMARY KEY (dwarf_id, equipment_id)
);

CREATE TABLE Workshop_Craftsdwarves (
    workshop_id INTEGER NOT NULL REFERENCES Workshops (workshop_id),
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    assignment_date TEXT NOT NULL,
    role TEXT NOT NULL,
    PRIMARY KEY (workshop_id, dwarf_id)
);

CREATE TABLE Workshop_Materials (
    workshop_id INTEGER NOT NULL REFERENCES Workshops (workshop_id),
    material_id INTEGER NOT NULL REFERENCES Resources (resource_id),
    is_input INTEGER NOT NULL DEFAULT 1,
    quantity INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (workshop_id, material_id)
);

CREATE TABLE Workshop_Products (
    workshop_id INTEGER NOT NULL REFERENCES Workshops (workshop_id),
    product_id INTEGER NOT NULL REFERENCES Products (product_id),
    production_date TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (workshop_id, product_id)
);

CREATE TABLE Traders (
    trader_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    race TEXT NOT NULL,
    caravan_id INTEGER NOT NULL REFERENCES Caravans (caravan_id),
    specialty TEXT
);

CREATE TABLE Caravan_Goods (
    goods_id INTEGER PRIMARY KEY,
    caravan_id INTEGER NOT NULL REFERENCES Caravans (caravan_id),
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    value INTEGER NOT NULL DEFAULT 0,
    material_type TEXT,
    price_fluctuation REAL NOT NULL DEFAULT 1.0,
    original_product_id INTEGER REFERENCES Products (product_id)
);

CREATE TABLE Trade_Transactions (
    transaction_id INTEGER PRIMARY KEY,
    caravan_id INTEGER NOT NULL REFERENCES Caravans (caravan_id),
    date TEXT NOT NULL,
    fortress_items TEXT,
    caravan_items TEXT,
    value INTEGER NOT NULL DEFAULT 0,
    balance_direction TEXT NOT NULL
);

CREATE TABLE Dwarf_Interests (
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    goods_type TEXT NOT NULL,
    interest_level INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (dwarf_id, goods_type)
);

CREATE TABLE Diplomatic_Events (
    event_id INTEGER PRIMARY KEY,
    caravan_id INTEGER NOT NULL REFERENCES Caravans (caravan_id),
    TYPE TEXT NOT NULL,
    outcome TEXT NOT NULL,
    date TEXT NOT NULL,
    relationship_change INTEGER NOT NULL DEFAULT 0,
    civilization_type TEXT NOT NULL
);

CREATE TABLE Creature_Sightings (
    sighting_id INTEGER PRIMARY KEY,
    creature_id INTEGER NOT NULL REFERENCES Creatures (creature_id),
    location TEXT NOT NULL,
    date TEXT NOT NULL,
    witness_id INTEGER REFERENCES Dwarves (dwarf_id)
);

CREATE TABLE Creature_Attacks (
    attack_id INTEGER PRIMARY KEY,
    creature_id INTEGER NOT NULL REFERENCES Creatures (creature_id),
    date TEXT NOT NULL,
    casualties INTEGER NOT NULL DEFAULT 0,
    enemy_casualties INTEGER NOT NULL DEFAULT 0,
    location_id INTEGER REFERENCES Locations (location_id),
    outcome TEXT NOT NULL,
    defense_structures_used TEXT,
    military_response_time_minutes INTEGER
);

CREATE TABLE Creature_Territories (
    territory_id INTEGER PRIMARY KEY,
    creature_id INTEGER NOT NULL REFERENCES Creatures (creature_id),
    area TEXT NOT NULL,
    danger_level INTEGER NOT NULL,
    distance_to_fortress INTEGER NOT NULL
);

CREATE TABLE Expedition_Members (
    expedition_id INTEGER NOT NULL REFERENCES Expeditions (expedition_id),
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    role TEXT NOT NULL,
    survived INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (expedition_id, dwarf_id)
);

CREATE TABLE Expedition_Sites (
    expedition_id INTEGER NOT NULL REFERENCES Expeditions (expedition_id),
    site_id INTEGER NOT NULL REFERENCES Extraction_Sites (site_id),
    discovery_date TEXT NOT NULL,
    notes TEXT,
    PRIMARY KEY (expedition_id, site_id)
);

CREATE TABLE Expedition_Creatures (
    expedition_id INTEGER NOT NULL REFERENCES Expeditions (expedition_id),
    creature_id INTEGER NOT NULL REFERENCES Creatures (creature_id),
    encounter_date TEXT NOT NULL,
    outcome TEXT NOT NULL,
    PRIMARY KEY (expedition_id, creature_id)
);

CREATE TABLE Expedition_Equipment (
    expedition_id INTEGER NOT NULL REFERENCES Expeditions (expedition_id),
    equipment_id INTEGER NOT NULL REFERENCES Equipment (equipment_id),
    quantity INTEGER NOT NULL DEFAULT 1,
    return_condition TEXT,
    PRIMARY KEY (expedition_id, equipment_id)
);

CREATE TABLE Expedition_Artifacts (
    artifact_id INTEGER PRIMARY KEY,
    expedition_id INTEGER NOT NULL REFERENCES Expeditions (expedition_id),
    discovery_date TEXT NOT NULL,
    value INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE Expedition_Reports (
    report_id INTEGER PRIMARY KEY,
    expedition_id INTEGER NOT NULL REFERENCES Expeditions (expedition_id),
    author_id INTEGER REFERENCES Dwarves (dwarf_id),
    title TEXT NOT NULL,
    content TEXT,
    creation_date TEXT NOT NULL
);

CREATE TABLE Projects (
    project_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    TYPE TEXT NOT NULL,
    STATUS TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 1,
    workshop_id INTEGER REFERENCES Workshops (workshop_id)
);

CREATE TABLE Squad_Members (
    squad_id INTEGER NOT NULL REFERENCES Military_Squads (squad_id),
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    join_date TEXT NOT NULL,
    role TEXT NOT NULL,
    exit_date TEXT,
    exit_reason TEXT,
    PRIMARY KEY (squad_id, dwarf_id)
);

CREATE TABLE Squad_Operations (
    operation_id INTEGER PRIMARY KEY,
    squad_id INTEGER NOT NULL REFERENCES Military_Squads (squad_id),
    TYPE TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    STATUS TEXT NOT NULL
);

CREATE TABLE Squad_Training (
    schedule_id INTEGER PRIMARY KEY,
    squad_id INTEGER NOT NULL REFERENCES Military_Squads (squad_id),
    TYPE TEXT NOT NULL,
    frequency TEXT NOT NULL,
    location_id INTEGER REFERENCES Locations (location_id),
    effectiveness INTEGER NOT NULL DEFAULT 50,
    duration_hours INTEGER NOT NULL DEFAULT 2,
    date TEXT NOT NULL
);

CREATE TABLE Squad_Battles (
    report_id INTEGER PRIMARY KEY,
    squad_id INTEGER NOT NULL REFERENCES Military_Squads (squad_id),
    date TEXT NOT NULL,
    outcome TEXT NOT NULL,
    enemy_type TEXT NOT NULL,
    casualties INTEGER NOT NULL DEFAULT 0,
    enemy_casualties INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE Squad_Equipment (
    squad_id INTEGER NOT NULL REFERENCES Military_Squads (squad_id),
    equipment_id INTEGER NOT NULL REFERENCES Equipment (equipment_id),
    quantity INTEGER NOT NULL DEFAULT 1,
    issued_date TEXT NOT NULL,
    PRIMARY KEY (squad_id, equipment_id)
);

CREATE TABLE Military_Stations (
    station_id INTEGER PRIMARY KEY,
    squad_id INTEGER REFERENCES Military_Squads (squad_id),
    location_id INTEGER REFERENCES Locations (location_id),
    assigned_date TEXT NOT NULL,
    STATUS TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE Squad_Movement (
    movement_id INTEGER PRIMARY KEY,
    squad_id INTEGER NOT NULL REFERENCES Military_Squads (squad_id),
    location_id INTEGER REFERENCES Locations (location_id),
    date TEXT NOT NULL,
    purpose TEXT
);

CREATE TABLE Military_Coverage_Zones (
    coverage_id INTEGER PRIMARY KEY,
    squad_id INTEGER NOT NULL REFERENCES Military_Squads (squad_id),
    location_id INTEGER REFERENCES Locations (location_id),
    response_time INTEGER NOT NULL DEFAULT 5,
    coverage_level TEXT NOT NULL DEFAULT 'normal'
);

CREATE TABLE Project_Workers (
    project_id INTEGER NOT NULL REFERENCES Projects (project_id),
    dwarf_id INTEGER NOT NULL REFERENCES Dwarves (dwarf_id),
    assignment_date TEXT NOT NULL,
    role TEXT NOT NULL,
    PRIMARY KEY (project_id, dwarf_id)
);

CREATE TABLE Project_Materials (
    project_id INTEGER NOT NULL REFERENCES Projects (project_id),
    material_id INTEGER NOT NULL REFERENCES Resources (resource_id),
    quantity_required INTEGER NOT NULL DEFAULT 0,
    quantity_available INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (project_id, material_id)
);

CREATE TABLE Project_Dependencies (
    project_id INTEGER NOT NULL REFERENCES Projects (project_id),
    dependent_project_id INTEGER NOT NULL REFERENCES Projects (project_id),
    dependency_type TEXT NOT NULL,
    PRIMARY KEY (project_id, dependent_project_id)
);

CREATE TABLE Project_Zones (
    zone_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES Projects (project_id),
    area TEXT NOT NULL,
    purpose TEXT NOT NULL
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES Projects (project_id),
    description TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    priority INTEGER NOT NULL DEFAULT 1,
    STATUS TEXT NOT NULL
);

INSERT INTO
    Fortresses (
        fortress_id,
        name,
        location,
        founded_year,
        depth,
        population
    )
VALUES
    (
        1,
        'Mountainhome',
        'Eastern Mountains',
        205,
        50,
        120
    ),
    (2, 'Deeprock', 'Northern Peaks', 310, 80, 75);

INSERT INTO
    Resources (resource_id, name, TYPE, rarity, description)
VALUES
    (
        1,
        'Iron Ore',
        'metal',
        'common',
        'Raw iron for smelting'
    ),
    (
        2,
        'Granite',
        'stone',
        'common',
        'Hard building stone'
    ),
    (3, 'Coal', 'fuel', 'common', 'Fuel for forges'),
    (
        4,
        'Gold',
        'metal',
        'rare',
        'Precious metal for trade'
    ),
    (
        5,
        'Copper Ore',
        'metal',
        'common',
        'Soft metal, good for tools'
    );

INSERT INTO
    Skills (
        skill_id,
        name,
        category,
        description,
        skill_type
    )
VALUES
    (
        1,
        'Mining',
        'labor',
        'Extracting ores and stone',
        'manual'
    ),
    (
        2,
        'Smithing',
        'crafting',
        'Forging metal items',
        'crafting'
    ),
    (
        3,
        'Combat',
        'military',
        'Melee fighting',
        'military'
    ),
    (
        4,
        'Carpentry',
        'crafting',
        'Woodworking',
        'crafting'
    ),
    (
        5,
        'Farming',
        'labor',
        'Growing crops underground',
        'manual'
    );

INSERT INTO
    Creatures (
        creature_id,
        name,
        TYPE,
        threat_level,
        active,
        estimated_population
    )
VALUES
    (1, 'Cave Spider', 'spider', 3, 1, 20),
    (2, 'Goblin Raider', 'goblin', 6, 1, 50),
    (3, 'Dragon', 'dragon', 10, 0, 1),
    (4, 'Giant Bat', 'beast', 2, 1, 15);

INSERT INTO
    Locations (
        location_id,
        zone_id,
        name,
        zone_type,
        depth,
        access_points,
        fortification_level,
        wall_integrity,
        trap_density,
        choke_points
    )
VALUES
    (1, 1, 'Main Gate', 'entrance', 0, 3, 8, 95, 5, 2),
    (
        2,
        1,
        'Iron Mine East',
        'mine',
        30,
        1,
        2,
        80,
        1,
        0
    ),
    (
        3,
        2,
        'Forge Hall',
        'workshop',
        10,
        2,
        3,
        90,
        0,
        1
    ),
    (4, 2, 'Barracks', 'military', 5, 2, 6, 100, 2, 1),
    (5, 3, 'Deep Tunnels', 'mine', 70, 1, 0, 60, 0, 0);

INSERT INTO
    Weather_Records (record_id, date, condition, temperature, notes)
VALUES
    (1, '400-03-01', 'clear', 12, NULL),
    (
        2,
        '400-06-15',
        'stormy',
        5,
        'Heavy rain, no caravans'
    ),
    (3, '400-09-20', 'clear', 8, NULL);

INSERT INTO
    Moon_Phases (phase_id, date, phase, illumination)
VALUES
    (1, '400-03-01', 'full', 100),
    (2, '400-03-08', 'waning', 50),
    (3, '400-03-15', 'new', 0);

INSERT INTO
    Security_Recommendations (
        recommendation_id,
        title,
        description,
        priority,
        STATUS
    )
VALUES
    (
        1,
        'Reinforce Main Gate',
        'Add drawbridge mechanism',
        1,
        'open'
    ),
    (
        2,
        'Trap Deep Tunnels',
        'Install cage traps at 70-depth junction',
        2,
        'in_progress'
    );

INSERT INTO
    Dwarves (dwarf_id, name, age, profession, fortress_id)
VALUES
    (1, 'Urist McAxe', 45, 'miner', 1),
    (2, 'Doren Bronzehead', 32, 'carpenter', 1),
    (3, 'Morul Stonepick', 28, 'miner', 1),
    (4, 'Sibrek Hammerman', 67, 'warrior', 1),
    (5, 'Etur Craftstone', 51, 'blacksmith', 1),
    (6, 'Zulban Geargrind', 38, 'miner', 2),
    (7, 'Medtob Ironwill', 22, 'farmer', 2),
    (8, 'Kadol Swiftpick', 55, 'warrior', 2),
    (9, 'Tun Stonecarver', 19, 'carpenter', 1),
    (10, 'Vucar Deepmine', 44, 'miner', 2);

INSERT INTO
    Equipment (equipment_id, name, TYPE, material_id, quality)
VALUES
    (1, 'Iron Pickaxe', 'tool', 1, 'fine'),
    (2, 'Steel Sword', 'weapon', 1, 'masterwork'),
    (3, 'Iron Shield', 'armor', 1, 'standard'),
    (4, 'War Hammer', 'weapon', 1, 'fine'),
    (5, 'Copper Axe', 'weapon', 5, 'standard');

INSERT INTO
    Extraction_Sites (
        site_id,
        name,
        TYPE,
        resource_id,
        depth,
        accessibility
    )
VALUES
    (
        1,
        'Eastern Iron Vein',
        'mine',
        1,
        30,
        'moderate'
    ),
    (
        2,
        'Northern Coal Seam',
        'mine',
        3,
        45,
        'difficult'
    ),
    (
        3,
        'Gold Pocket',
        'mine',
        4,
        60,
        'very difficult'
    ),
    (4, 'Granite Quarry', 'quarry', 2, 5, 'easy');

INSERT INTO
    Fortress_Resources (
        fortress_id,
        resource_id,
        quantity,
        discovery_date
    )
VALUES
    (1, 1, 500, '205-03-15'),
    (1, 2, 1200, '205-01-01'),
    (1, 3, 300, '206-07-20'),
    (2, 1, 200, '310-05-10'),
    (2, 4, 50, '315-11-01');

INSERT INTO
    Workshops (workshop_id, name, TYPE, quality, fortress_id)
VALUES
    (1, 'Main Forge', 'forge', 'fine', 1),
    (2, 'Carpenter Hall', 'carpentry', 'standard', 1),
    (3, 'Deep Smelter', 'smelter', 'masterwork', 2);

INSERT INTO
    Stockpile_Contents (stockpile_id, resource_id, quantity, quality)
VALUES
    (1, 1, 150, 'raw'),
    (2, 2, 400, 'cut'),
    (3, 3, 80, 'raw'),
    (4, 4, 10, 'refined');

INSERT INTO
    Caravans (
        caravan_id,
        arrival_date,
        departure_date,
        civilization_type,
        fortress_id
    )
VALUES
    (1, '400-04-01', '400-04-15', 'human', 1),
    (2, '400-08-10', '400-08-25', 'elven', 1),
    (3, '401-03-20', NULL, 'dwarven', 2);

INSERT INTO
    Expeditions (
        expedition_id,
        destination,
        departure_date,
        return_date,
        STATUS
    )
VALUES
    (
        1,
        'Eastern Caves',
        '399-05-01',
        '399-06-15',
        'completed'
    ),
    (2, 'Dragon Peaks', '400-02-10', NULL, 'ongoing');

INSERT INTO
    Fortress_Events (
        event_id,
        fortress_id,
        TYPE,
        date,
        description,
        severity
    )
VALUES
    (
        1,
        1,
        'attack',
        '399-09-12',
        'Goblin siege repelled at main gate',
        'high'
    ),
    (
        2,
        1,
        'trade',
        '400-04-01',
        'Human caravan arrived with fine goods',
        'low'
    ),
    (
        3,
        2,
        'discovery',
        '400-01-15',
        'Gold vein discovered at depth 60',
        'medium'
    );

INSERT INTO
    Defense_Structures (
        structure_id,
        name,
        TYPE,
        location_id,
        integrity,
        construction_date
    )
VALUES
    (
        1,
        'Iron Drawbridge',
        'drawbridge',
        1,
        95,
        '210-04-01'
    ),
    (2, 'Spike Trap Row', 'trap', 1, 80, '215-06-15'),
    (
        3,
        'Stone Wall East',
        'wall',
        2,
        100,
        '220-02-10'
    );

INSERT INTO
    Military_Squads (
        squad_id,
        name,
        formation_type,
        leader_id,
        fortress_id
    )
VALUES
    (1, 'Iron Hammers', 'shield wall', 4, 1),
    (2, 'Deep Axes', 'skirmish', 8, 2),
    (3, 'Ghost Patrol', 'scout', NULL, 1);

INSERT INTO
    Products (
        product_id,
        name,
        TYPE,
        quality,
        material_id,
        value,
        created_by,
        workshop_id
    )
VALUES
    (1, 'Iron Helm', 'armor', 'fine', 1, 120, 5, 1),
    (
        2,
        'Oak Chair',
        'furniture',
        'standard',
        2,
        40,
        2,
        2
    ),
    (
        3,
        'Iron Ingot',
        'material',
        'standard',
        1,
        30,
        5,
        3
    );

INSERT INTO
    Dwarf_Skills (dwarf_id, skill_id, LEVEL, experience, date)
VALUES
    (1, 1, 8, 4200, '395-01-01'),
    (2, 4, 6, 2800, '396-03-10'),
    (3, 1, 4, 1500, '397-07-20'),
    (4, 3, 9, 6000, '380-05-05'),
    (5, 2, 10, 8500, '370-11-01'),
    (6, 1, 5, 2000, '398-02-14'),
    (7, 5, 3, 900, '399-08-30'),
    (8, 3, 7, 4800, '385-04-17'),
    (9, 4, 2, 600, '399-12-01'),
    (10, 1, 6, 3100, '393-09-09');

INSERT INTO
    Dwarf_Assignments (
        assignment_id,
        dwarf_id,
        assignment_type,
        start_date,
        end_date
    )
VALUES
    (1, 1, 'mining', '400-01-01', NULL),
    (2, 2, 'carpentry', '400-01-01', NULL),
    (3, 4, 'patrol', '400-01-01', NULL),
    (4, 5, 'smithing', '400-01-01', NULL),
    (5, 7, 'farming', '400-01-01', NULL);

INSERT INTO
    Dwarf_Equipment (dwarf_id, equipment_id, quality, equipped_date)
VALUES
    (1, 1, 'fine', '400-01-10'),
    (4, 2, 'masterwork', '395-03-20'),
    (4, 3, 'standard', '395-03-20'),
    (8, 4, 'fine', '398-07-01'),
    (3, 5, 'standard', '400-02-15');

INSERT INTO
    Workshop_Craftsdwarves (workshop_id, dwarf_id, assignment_date, role)
VALUES
    (1, 5, '400-01-01', 'master'),
    (2, 2, '400-01-01', 'master'),
    (2, 9, '400-03-01', 'apprentice'),
    (3, 5, '400-01-01', 'master');

INSERT INTO
    Workshop_Materials (workshop_id, material_id, is_input, quantity)
VALUES
    (1, 1, 1, 200),
    (1, 3, 1, 50),
    (3, 1, 1, 100),
    (3, 3, 1, 80);

INSERT INTO
    Workshop_Products (
        workshop_id,
        product_id,
        production_date,
        quantity
    )
VALUES
    (1, 1, '400-02-20', 3),
    (2, 2, '400-03-05', 5),
    (3, 3, '400-01-25', 20);

INSERT INTO
    Traders (trader_id, name, race, caravan_id, specialty)
VALUES
    (1, 'Aldric the Merchant', 'human', 1, 'weapons'),
    (2, 'Seraphina Goldleaf', 'human', 1, 'food'),
    (3, 'Silverwind', 'elf', 2, 'wood'),
    (4, 'Bofri Ironpurse', 'dwarf', 3, 'gems');

INSERT INTO
    Caravan_Goods (
        goods_id,
        caravan_id,
        name,
        TYPE,
        quantity,
        value,
        material_type,
        price_fluctuation
    )
VALUES
    (
        1,
        1,
        'Steel Sword',
        'import',
        5,
        200,
        'steel',
        1.1
    ),
    (
        2,
        1,
        'Wheat Flour',
        'import',
        30,
        15,
        'food',
        0.9
    ),
    (
        3,
        2,
        'Elvish Bow',
        'import',
        3,
        350,
        'wood',
        1.2
    ),
    (
        4,
        3,
        'Cut Diamond',
        'import',
        2,
        800,
        'gem',
        1.5
    );

INSERT INTO
    Trade_Transactions (
        transaction_id,
        caravan_id,
        date,
        fortress_items,
        caravan_items,
        value,
        balance_direction
    )
VALUES
    (
        1,
        1,
        '400-04-10',
        'iron ingots x20',
        'wheat flour x30',
        600,
        'export'
    ),
    (
        2,
        2,
        '400-08-18',
        'granite blocks x50',
        'elvish bow x1',
        350,
        'import'
    );

INSERT INTO
    Dwarf_Interests (dwarf_id, goods_type, interest_level)
VALUES
    (4, 'weapons', 5),
    (5, 'tools', 4),
    (2, 'furniture', 3),
    (1, 'tools', 5),
    (8, 'armor', 4);

INSERT INTO
    Diplomatic_Events (
        event_id,
        caravan_id,
        TYPE,
        outcome,
        date,
        relationship_change,
        civilization_type
    )
VALUES
    (
        1,
        1,
        'trade_meeting',
        'positive',
        '400-04-01',
        10,
        'human'
    ),
    (
        2,
        2,
        'gift_exchange',
        'positive',
        '400-08-12',
        5,
        'elven'
    ),
    (
        3,
        3,
        'dispute',
        'negative',
        '401-03-21',
        -3,
        'dwarven'
    );

INSERT INTO
    Creature_Sightings (
        sighting_id,
        creature_id,
        location,
        date,
        witness_id
    )
VALUES
    (1, 1, 'Deep Tunnels Level 3', '400-02-14', 3),
    (2, 2, 'Eastern Forest Edge', '399-08-30', 4),
    (3, 4, 'Cave Entrance North', '400-05-07', 1),
    (4, 1, 'Iron Mine East Shaft', '400-06-20', 6);

INSERT INTO
    Creature_Attacks (
        attack_id,
        creature_id,
        date,
        casualties,
        enemy_casualties,
        location_id,
        outcome,
        defense_structures_used,
        military_response_time_minutes
    )
VALUES
    (
        1,
        2,
        '399-09-12',
        1,
        8,
        1,
        'repelled',
        'Iron Drawbridge, Spike Trap Row',
        12
    ),
    (2, 1, '400-06-22', 0, 3, 2, 'repelled', NULL, 25),
    (3, 4, '400-05-08', 0, 1, 1, 'repelled', NULL, 8);

INSERT INTO
    Creature_Territories (
        territory_id,
        creature_id,
        area,
        danger_level,
        distance_to_fortress
    )
VALUES
    (1, 1, 'Deep Tunnels below level 5', 3, 300),
    (2, 2, 'Eastern Forest', 6, 2000),
    (3, 3, 'Dragon Peaks', 10, 8000),
    (4, 4, 'Cave Network North', 2, 500);

INSERT INTO
    Expedition_Members (expedition_id, dwarf_id, role, survived)
VALUES
    (1, 3, 'scout', 1),
    (1, 9, 'mapper', 1),
    (2, 1, 'lead miner', 1),
    (2, 6, 'guard', 1);

INSERT INTO
    Expedition_Sites (expedition_id, site_id, discovery_date, notes)
VALUES
    (
        1,
        1,
        '399-05-20',
        'Large iron deposit, accessible'
    ),
    (
        2,
        3,
        '400-03-01',
        'Gold pocket confirmed, dangerous approach'
    );

INSERT INTO
    Expedition_Creatures (
        expedition_id,
        creature_id,
        encounter_date,
        outcome
    )
VALUES
    (1, 1, '399-05-18', 'fled'),
    (2, 3, '400-02-28', 'avoided');

INSERT INTO
    Expedition_Equipment (
        expedition_id,
        equipment_id,
        quantity,
        return_condition
    )
VALUES
    (1, 1, 2, 'worn'),
    (1, 5, 1, 'good'),
    (2, 1, 3, NULL),
    (2, 2, 2, NULL);

INSERT INTO
    Expedition_Artifacts (
        artifact_id,
        expedition_id,
        discovery_date,
        value
    )
VALUES
    (1, 1, '399-06-01', 250),
    (2, 2, '400-03-10', 1200);

INSERT INTO
    Expedition_Reports (
        report_id,
        expedition_id,
        author_id,
        title,
        content,
        creation_date
    )
VALUES
    (
        1,
        1,
        3,
        'Eastern Caves Survey',
        'Iron deposit found at depth 30. Cave spiders present but manageable.',
        '399-06-20'
    ),
    (
        2,
        2,
        1,
        'Dragon Peaks Preliminary',
        'Gold confirmed. Dragon territory nearby. Recommend armed escort for extraction.',
        '400-03-15'
    );

INSERT INTO
    Projects (
        project_id,
        name,
        TYPE,
        STATUS,
        priority,
        workshop_id
    )
VALUES
    (
        1,
        'Expand Iron Mine',
        'mining',
        'active',
        1,
        NULL
    ),
    (
        2,
        'Forge Squad Armor',
        'crafting',
        'active',
        2,
        1
    ),
    (
        3,
        'Build Guard Tower',
        'construction',
        'planned',
        3,
        NULL
    );

INSERT INTO
    Squad_Members (
        squad_id,
        dwarf_id,
        join_date,
        role,
        exit_date,
        exit_reason
    )
VALUES
    (1, 4, '380-01-01', 'leader', NULL, NULL),
    (1, 3, '399-03-15', 'soldier', NULL, NULL),
    (2, 8, '385-06-10', 'leader', NULL, NULL),
    (2, 6, '400-01-20', 'soldier', NULL, NULL),
    (3, 9, '400-04-01', 'scout', NULL, NULL);

INSERT INTO
    Squad_Operations (
        operation_id,
        squad_id,
        TYPE,
        start_date,
        end_date,
        STATUS
    )
VALUES
    (1, 1, 'patrol', '400-01-01', NULL, 'ongoing'),
    (2, 2, 'mine_guard', '400-01-01', NULL, 'ongoing'),
    (
        3,
        1,
        'siege_defense',
        '399-09-12',
        '399-09-12',
        'completed'
    );

INSERT INTO
    Squad_Training (
        schedule_id,
        squad_id,
        TYPE,
        frequency,
        location_id,
        effectiveness,
        duration_hours,
        date
    )
VALUES
    (
        1,
        1,
        'melee_drill',
        'daily',
        4,
        75,
        3,
        '400-01-05'
    ),
    (
        2,
        2,
        'axe_practice',
        'daily',
        4,
        70,
        2,
        '400-01-05'
    ),
    (3, 3, 'stealth', 'weekly', 5, 60, 4, '400-01-07');

INSERT INTO
    Squad_Battles (
        report_id,
        squad_id,
        date,
        outcome,
        enemy_type,
        casualties,
        enemy_casualties
    )
VALUES
    (1, 1, '399-09-12', 'victory', 'goblin', 1, 8),
    (
        2,
        2,
        '400-06-22',
        'victory',
        'cave_spider',
        0,
        3
    );

INSERT INTO
    Squad_Equipment (squad_id, equipment_id, quantity, issued_date)
VALUES
    (1, 2, 3, '395-01-15'),
    (1, 3, 3, '395-01-15'),
    (2, 4, 2, '398-03-20'),
    (2, 5, 2, '398-03-20');

INSERT INTO
    Military_Stations (
        station_id,
        squad_id,
        location_id,
        assigned_date,
        STATUS
    )
VALUES
    (1, 1, 1, '400-01-01', 'active'),
    (2, 2, 2, '400-01-01', 'active'),
    (3, 3, 5, '400-04-01', 'active');

INSERT INTO
    Squad_Movement (
        movement_id,
        squad_id,
        location_id,
        date,
        purpose
    )
VALUES
    (1, 1, 1, '400-01-01', 'gate_patrol'),
    (2, 1, 5, '400-03-10', 'deep_check'),
    (3, 2, 2, '400-01-01', 'mine_guard');

INSERT INTO
    Military_Coverage_Zones (
        coverage_id,
        squad_id,
        location_id,
        response_time,
        coverage_level
    )
VALUES
    (1, 1, 1, 2, 'high'),
    (2, 1, 3, 5, 'normal'),
    (3, 2, 2, 3, 'high'),
    (4, 3, 5, 10, 'low');

INSERT INTO
    Project_Workers (project_id, dwarf_id, assignment_date, role)
VALUES
    (1, 1, '400-03-01', 'lead miner'),
    (1, 3, '400-03-01', 'miner'),
    (2, 5, '400-04-01', 'smith'),
    (3, 2, '400-05-01', 'carpenter');

INSERT INTO
    Project_Materials (
        project_id,
        material_id,
        quantity_required,
        quantity_available
    )
VALUES
    (1, 3, 100, 80),
    (2, 1, 200, 150),
    (3, 2, 500, 500);

INSERT INTO
    Project_Dependencies (
        project_id,
        dependent_project_id,
        dependency_type
    )
VALUES
    (2, 1, 'material'),
    (3, 1, 'access');

INSERT INTO
    Project_Zones (zone_id, project_id, area, purpose)
VALUES
    (
        1,
        1,
        'East shaft depth 30-50',
        'primary extraction'
    ),
    (2, 3, 'Main Gate exterior', 'construction site');

INSERT INTO
    Orders (
        order_id,
        project_id,
        description,
        creation_date,
        priority,
        STATUS
    )
VALUES
    (
        1,
        1,
        'Blast through granite layer at depth 35',
        '400-03-01',
        1,
        'active'
    ),
    (
        2,
        2,
        'Produce 5 sets of iron armor',
        '400-04-01',
        2,
        'active'
    ),
    (
        3,
        3,
        'Survey and mark tower foundation',
        '400-05-01',
        3,
        'pending'
    );

-- 2
SELECT
    d.dwarf_id,
    d.name,
    d.age,
    d.profession,
    JSON_OBJECT(
        'skill_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(ds.skill_id)
            FROM
                Dwarf_Skills ds
            WHERE
                ds.dwarf_id = d.dwarf_id
        ),
        'assignment_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(da.assignment_id)
            FROM
                Dwarf_Assignments da
            WHERE
                da.dwarf_id = d.dwarf_id
        ),
        'squad_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(sm.squad_id)
            FROM
                Squad_Members sm
            WHERE
                sm.dwarf_id = d.dwarf_id
        ),
        'equipment_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(de.equipment_id)
            FROM
                Dwarf_Equipment de
            WHERE
                de.dwarf_id = d.dwarf_id
        )
    ) AS related_entities
FROM
    Dwarves d;

-- 4
SELECT
    w.workshop_id,
    w.name,
    w.type,
    w.quality,
    JSON_OBJECT(
        'craftsdwarf_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(wc.dwarf_id)
            FROM
                Workshop_Craftsdwarves wc
            WHERE
                wc.workshop_id = w.workshop_id
        ),
        'project_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(p.project_id)
            FROM
                Projects p
            WHERE
                p.workshop_id = w.workshop_id
        ),
        'input_material_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(wm.material_id)
            FROM
                Workshop_Materials wm
            WHERE
                wm.workshop_id = w.workshop_id
                AND wm.is_input = 1
        ),
        'output_product_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(wp.product_id)
            FROM
                Workshop_Products wp
            WHERE
                wp.workshop_id = w.workshop_id
        )
    ) AS related_entities
FROM
    Workshops w;

-- 4
SELECT
    s.squad_id,
    s.name,
    s.formation_type,
    s.leader_id,
    JSON_OBJECT(
        'member_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(sm.dwarf_id)
            FROM
                Squad_Members sm
            WHERE
                sm.squad_id = s.squad_id
        ),
        'equipment_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(se.equipment_id)
            FROM
                Squad_Equipment se
            WHERE
                se.squad_id = s.squad_id
        ),
        'operation_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(so.operation_id)
            FROM
                Squad_Operations so
            WHERE
                so.squad_id = s.squad_id
        ),
        'training_schedule_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(st.schedule_id)
            FROM
                Squad_Training st
            WHERE
                st.squad_id = s.squad_id
        ),
        'battle_report_ids',
        (
            SELECT
                JSON_GROUP_ARRAY(sb.report_id)
            FROM
                Squad_Battles sb
            WHERE
                sb.squad_id = s.squad_id
        )
    ) AS related_entities
FROM
    Military_Squads s;
