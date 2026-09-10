WITH threat_stats AS (
    SELECT
        c.creature_id,
        c.name AS creature_name,
        c.type AS creature_type,
        c.threat_level,
        c.estimated_population,
        (
            SELECT
                MAX(cs.date)
            FROM
                Creature_Sightings cs
            WHERE
                cs.creature_id = c.creature_id
        ) AS last_sighting,
        (
            SELECT
                ROUND(
                    CAST(MIN(ct.distance_to_fortress) AS REAL) / 1000.0,
                    1
                )
            FROM
                Creature_Territories ct
            WHERE
                ct.creature_id = c.creature_id
        ) AS territory_proximity_km
    FROM
        Creatures c
    WHERE
        c.active = 1
),
vuln_stats AS (
    SELECT
        l.location_id,
        l.zone_id,
        l.name AS zone_name,
        l.fortification_level,
        ROUND(
            MIN(CAST(l.access_points AS REAL), 5.0) / 5.0 * 0.20 + (10.0 - MIN(l.fortification_level, 10)) / 10.0 * 0.30 + (100.0 - l.wall_integrity) / 100.0 * 0.25 + (10.0 - MIN(l.trap_density, 10)) / 10.0 * 0.15 + (5.0 - MIN(l.choke_points, 5)) / 5.0 * 0.10,
            2
        ) AS vulnerability_score,
        (
            SELECT
                COUNT(*)
            FROM
                Creature_Attacks ca
            WHERE
                ca.location_id = l.location_id
                AND ca.outcome != 'repelled'
        ) AS historical_breaches,
        (
            SELECT
                CAST(
                    ROUND(AVG(ca.military_response_time_minutes)) AS INTEGER
                )
            FROM
                Creature_Attacks ca
            WHERE
                ca.location_id = l.location_id
        ) AS avg_response_time
    FROM
        Locations l
),
defense_type_eff AS (
    SELECT
        ds.type AS defense_type,
        ROUND(
            CAST(
                SUM(
                    CASE
                        WHEN ca.outcome = 'repelled' THEN 1
                        ELSE 0
                    END
                ) AS REAL
            ) / NULLIF(COUNT(ca.attack_id), 0) * 100,
            2
        ) AS effectiveness_rate,
        ROUND(AVG(CAST(ca.enemy_casualties AS REAL)), 1) AS avg_enemy_casualties
    FROM
        Defense_Structures ds
        JOIN Creature_Attacks ca ON ca.location_id = ds.location_id
    GROUP BY
        ds.type
),
squad_base AS (
    SELECT
        s.squad_id,
        s.name AS squad_name,
        s.formation_type,
        (
            SELECT
                COUNT(*)
            FROM
                Squad_Members sm
            WHERE
                sm.squad_id = s.squad_id
                AND sm.exit_date IS NULL
        ) AS active_members,
        (
            SELECT
                COUNT(*)
            FROM
                Squad_Members sm
            WHERE
                sm.squad_id = s.squad_id
        ) AS total_members_ever,
        COALESCE(
            (
                SELECT
                    ROUND(AVG(ds.level), 2)
                FROM
                    Squad_Members sm
                    JOIN Dwarf_Skills ds ON ds.dwarf_id = sm.dwarf_id
                WHERE
                    sm.squad_id = s.squad_id
                    AND sm.exit_date IS NULL
            ),
            0
        ) AS avg_combat_skill,
        COALESCE(
            (
                SELECT
                    ROUND(
                        CAST(
                            SUM(
                                CASE
                                    WHEN sb.outcome = 'victory' THEN 1
                                    ELSE 0
                                END
                            ) AS REAL
                        ) / NULLIF(COUNT(*), 0),
                        2
                    )
                FROM
                    Squad_Battles sb
                WHERE
                    sb.squad_id = s.squad_id
            ),
            0
        ) AS combat_effectiveness,
        COALESCE(
            (
                SELECT
                    ROUND(AVG(st.effectiveness) / 100.0, 2)
                FROM
                    Squad_Training st
                WHERE
                    st.squad_id = s.squad_id
            ),
            0
        ) AS avg_training_eff
    FROM
        Military_Squads s
),
squad_readiness AS (
    SELECT
        *,
        ROUND(
            CAST(active_members AS REAL) / NULLIF(total_members_ever, 0) * 0.3 + avg_combat_skill / 10.0 * 0.4 + avg_training_eff * 0.3,
            2
        ) AS readiness_score
    FROM
        squad_base
),
yearly_base AS (
    SELECT
        CAST(SUBSTR(ca.date, 1, 3) AS INTEGER) AS attack_year,
        COUNT(*) AS total_attacks,
        SUM(ca.casualties) AS total_casualties,
        ROUND(
            CAST(
                SUM(
                    CASE
                        WHEN ca.outcome = 'repelled' THEN 1
                        ELSE 0
                    END
                ) AS REAL
            ) / COUNT(*) * 100,
            2
        ) AS defense_success_rate
    FROM
        Creature_Attacks ca
    GROUP BY
        attack_year
),
yearly_stats AS (
    SELECT
        attack_year,
        total_attacks,
        total_casualties,
        defense_success_rate,
        ROUND(
            defense_success_rate - LAG(defense_success_rate) OVER (
                ORDER BY
                    attack_year
            ),
            2
        ) AS year_over_year_improvement
    FROM
        yearly_base
)
SELECT
    JSON_OBJECT(
        'total_recorded_attacks',
        (
            SELECT
                COUNT(*)
            FROM
                Creature_Attacks
        ),
        'unique_attackers',
        (
            SELECT
                COUNT(DISTINCT creature_id)
            FROM
                Creature_Attacks
        ),
        'overall_defense_success_rate',
        (
            SELECT
                ROUND(
                    CAST(
                        SUM(
                            CASE
                                WHEN outcome = 'repelled' THEN 1
                                ELSE 0
                            END
                        ) AS REAL
                    ) / NULLIF(COUNT(*), 0) * 100,
                    2
                )
            FROM
                Creature_Attacks
        ),
        'security_analysis',
        JSON_OBJECT(
            'threat_assessment',
            JSON_OBJECT(
                'current_threat_level',
                (
                    SELECT
                        CASE
                            WHEN MAX(threat_level) >= 8 THEN 'Critical'
                            WHEN MAX(threat_level) >= 6 THEN 'High'
                            WHEN MAX(threat_level) >= 3 THEN 'Moderate'
                            ELSE 'Low'
                        END
                    FROM
                        threat_stats
                ),
                'active_threats',
                JSON(
                    COALESCE(
                        (
                            SELECT
                                JSON_GROUP_ARRAY(
                                    JSON_OBJECT(
                                        'creature_type',
                                        ts.creature_type,
                                        'threat_level',
                                        ts.threat_level,
                                        'last_sighting_date',
                                        ts.last_sighting,
                                        'territory_proximity',
                                        ts.territory_proximity_km,
                                        'estimated_numbers',
                                        ts.estimated_population,
                                        'creature_ids',
                                        JSON(
                                            (
                                                SELECT
                                                    JSON_GROUP_ARRAY(creature_id)
                                                FROM
                                                    Creatures
                                                WHERE
                                                    TYPE = ts.creature_type
                                                    AND active = 1
                                            )
                                        )
                                    )
                                )
                            FROM
                                (
                                    SELECT
                                        *
                                    FROM
                                        threat_stats
                                    ORDER BY
                                        threat_level DESC
                                ) ts
                        ),
                        '[]'
                    )
                )
            ),
            'vulnerability_analysis',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'zone_id',
                                    vs.zone_id,
                                    'zone_name',
                                    vs.zone_name,
                                    'vulnerability_score',
                                    vs.vulnerability_score,
                                    'historical_breaches',
                                    vs.historical_breaches,
                                    'fortification_level',
                                    vs.fortification_level,
                                    'military_response_time',
                                    vs.avg_response_time,
                                    'defense_coverage',
                                    JSON_OBJECT(
                                        'structure_ids',
                                        JSON(
                                            COALESCE(
                                                (
                                                    SELECT
                                                        JSON_GROUP_ARRAY(structure_id)
                                                    FROM
                                                        Defense_Structures
                                                    WHERE
                                                        location_id = vs.location_id
                                                ),
                                                '[]'
                                            )
                                        ),
                                        'squad_ids',
                                        JSON(
                                            COALESCE(
                                                (
                                                    SELECT
                                                        JSON_GROUP_ARRAY(squad_id)
                                                    FROM
                                                        Military_Coverage_Zones
                                                    WHERE
                                                        location_id = vs.location_id
                                                ),
                                                '[]'
                                            )
                                        )
                                    )
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    vuln_stats
                                ORDER BY
                                    vulnerability_score DESC
                            ) vs
                    ),
                    '[]'
                )
            ),
            'defense_effectiveness',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'defense_type',
                                    dte.defense_type,
                                    'effectiveness_rate',
                                    dte.effectiveness_rate,
                                    'avg_enemy_casualties',
                                    dte.avg_enemy_casualties,
                                    'structure_ids',
                                    JSON(
                                        (
                                            SELECT
                                                JSON_GROUP_ARRAY(structure_id)
                                            FROM
                                                Defense_Structures
                                            WHERE
                                                TYPE = dte.defense_type
                                        )
                                    )
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    defense_type_eff
                                ORDER BY
                                    effectiveness_rate DESC
                            ) dte
                    ),
                    '[]'
                )
            ),
            'military_readiness_assessment',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'squad_id',
                                    sr.squad_id,
                                    'squad_name',
                                    sr.squad_name,
                                    'readiness_score',
                                    sr.readiness_score,
                                    'active_members',
                                    sr.active_members,
                                    'avg_combat_skill',
                                    sr.avg_combat_skill,
                                    'combat_effectiveness',
                                    sr.combat_effectiveness,
                                    'response_coverage',
                                    JSON(
                                        COALESCE(
                                            (
                                                SELECT
                                                    JSON_GROUP_ARRAY(
                                                        JSON_OBJECT(
                                                            'zone_id',
                                                            mcz.location_id,
                                                            'response_time',
                                                            mcz.response_time
                                                        )
                                                    )
                                                FROM
                                                    Military_Coverage_Zones mcz
                                                WHERE
                                                    mcz.squad_id = sr.squad_id
                                            ),
                                            '[]'
                                        )
                                    )
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    squad_readiness
                                ORDER BY
                                    readiness_score DESC
                            ) sr
                    ),
                    '[]'
                )
            ),
            'security_evolution',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'year',
                                    ys.attack_year,
                                    'defense_success_rate',
                                    ys.defense_success_rate,
                                    'total_attacks',
                                    ys.total_attacks,
                                    'casualties',
                                    ys.total_casualties,
                                    'year_over_year_improvement',
                                    ys.year_over_year_improvement
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    yearly_stats
                                ORDER BY
                                    attack_year
                            ) ys
                    ),
                    '[]'
                )
            )
        )
    ) AS security_analysis;
