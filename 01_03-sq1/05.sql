WITH member_stats AS (
    SELECT
        em.expedition_id,
        COUNT(*) AS total_members,
        SUM(em.survived) AS survived_count,
        JSON_GROUP_ARRAY(em.dwarf_id) AS member_ids
    FROM
        Expedition_Members em
    GROUP BY
        em.expedition_id
),
artifact_stats AS (
    SELECT
        ea.expedition_id,
        COALESCE(SUM(ea.value), 0) AS artifacts_value,
        JSON_GROUP_ARRAY(ea.artifact_id) AS artifact_ids
    FROM
        Expedition_Artifacts ea
    GROUP BY
        ea.expedition_id
),
site_stats AS (
    SELECT
        es.expedition_id,
        COUNT(*) AS discovered_sites,
        JSON_GROUP_ARRAY(es.site_id) AS site_ids
    FROM
        Expedition_Sites es
    GROUP BY
        es.expedition_id
),
creature_stats AS (
    SELECT
        ec.expedition_id,
        COUNT(*) AS total_encounters,
        SUM(
            CASE
                WHEN ec.outcome IN ('fled', 'avoided', 'escaped') THEN 1
                ELSE 0
            END
        ) AS favorable_encounters
    FROM
        Expedition_Creatures ec
    GROUP BY
        ec.expedition_id
),
skill_stats AS (
    SELECT
        em.expedition_id,
        COALESCE(SUM(ds.experience), 0) AS skill_improvement
    FROM
        Expedition_Members em
        JOIN Dwarf_Skills ds ON ds.dwarf_id = em.dwarf_id
    GROUP BY
        em.expedition_id
)
SELECT
    e.expedition_id,
    e.destination,
    e.status,
    ROUND(
        CAST(COALESCE(ms.survived_count, 0) AS REAL) / COALESCE(ms.total_members, 1) * 100,
        2
    ) AS survival_rate,
    COALESCE(arts.artifacts_value, 0) AS artifacts_value,
    COALESCE(ss.discovered_sites, 0) AS discovered_sites,
    ROUND(
        CASE
            WHEN COALESCE(cs.total_encounters, 0) > 0 THEN CAST(cs.favorable_encounters AS REAL) / cs.total_encounters * 100
            ELSE 100.0
        END,
        2
    ) AS encounter_success_rate,
    COALESCE(sks.skill_improvement, 0) AS skill_improvement,
    CASE
        WHEN e.return_date IS NOT NULL THEN (
            CAST(SUBSTR(e.return_date, 1, 3) AS INTEGER) * 365 + CAST(SUBSTR(e.return_date, 5, 2) AS INTEGER) * 30 + CAST(SUBSTR(e.return_date, 8, 2) AS INTEGER)
        ) - (
            CAST(SUBSTR(e.departure_date, 1, 3) AS INTEGER) * 365 + CAST(SUBSTR(e.departure_date, 5, 2) AS INTEGER) * 30 + CAST(SUBSTR(e.departure_date, 8, 2) AS INTEGER)
        )
        ELSE NULL
    END AS expedition_duration,
    ROUND(
        (
            CAST(COALESCE(ms.survived_count, 0) AS REAL) / COALESCE(ms.total_members, 1) * 0.4
        ) + (
            CASE
                WHEN COALESCE(cs.total_encounters, 0) > 0 THEN CAST(cs.favorable_encounters AS REAL) / cs.total_encounters * 0.3
                ELSE 0.3
            END
        ) + (
            MIN(
                CAST(COALESCE(arts.artifacts_value, 0) AS REAL) / 1000.0,
                1.0
            ) * 0.2
        ) + (
            MIN(
                CAST(COALESCE(ss.discovered_sites, 0) AS REAL) / 3.0,
                1.0
            ) * 0.1
        ),
        2
    ) AS overall_success_score,
    JSON_OBJECT(
        'member_ids',
        JSON(COALESCE(ms.member_ids, '[]')),
        'artifact_ids',
        JSON(COALESCE(arts.artifact_ids, '[]')),
        'site_ids',
        JSON(COALESCE(ss.site_ids, '[]'))
    ) AS related_entities
FROM
    Expeditions e
    LEFT JOIN member_stats ms ON ms.expedition_id = e.expedition_id
    LEFT JOIN artifact_stats arts ON arts.expedition_id = e.expedition_id
    LEFT JOIN site_stats ss ON ss.expedition_id = e.expedition_id
    LEFT JOIN creature_stats cs ON cs.expedition_id = e.expedition_id
    LEFT JOIN skill_stats sks ON sks.expedition_id = e.expedition_id
ORDER BY
    overall_success_score DESC;
