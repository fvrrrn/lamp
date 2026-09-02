WITH battle_stats AS (
    SELECT
        squad_id,
        COUNT(*) AS total_battles,
        SUM(
            CASE
                WHEN outcome = 'victory' THEN 1
                ELSE 0
            END
        ) AS victories,
        ROUND(
            CAST(
                SUM(
                    CASE
                        WHEN outcome = 'victory' THEN 1
                        ELSE 0
                    END
                ) AS REAL
            ) / COUNT(*) * 100,
            2
        ) AS victory_percentage,
        SUM(casualties) AS total_casualties,
        SUM(enemy_casualties) AS total_enemy_casualties,
        ROUND(
            CAST(SUM(enemy_casualties) AS REAL) / NULLIF(SUM(casualties), 0),
            2
        ) AS casualty_exchange_ratio,
        JSON_GROUP_ARRAY(report_id) AS battle_report_ids
    FROM
        Squad_Battles
    GROUP BY
        squad_id
),
member_stats AS (
    SELECT
        squad_id,
        COUNT(*) AS total_members_ever,
        SUM(
            CASE
                WHEN exit_date IS NULL THEN 1
                ELSE 0
            END
        ) AS current_members,
        ROUND(
            CAST(
                SUM(
                    CASE
                        WHEN exit_date IS NULL THEN 1
                        ELSE 0
                    END
                ) AS REAL
            ) / COUNT(*) * 100,
            2
        ) AS retention_rate,
        JSON_GROUP_ARRAY(dwarf_id) AS member_ids
    FROM
        Squad_Members
    GROUP BY
        squad_id
),
equipment_stats AS (
    SELECT
        se.squad_id,
        ROUND(
            AVG(
                CASE
                    e.quality
                    WHEN 'legendary' THEN 8.0
                    WHEN 'masterwork' THEN 7.0
                    WHEN 'exceptional' THEN 6.0
                    WHEN 'superior' THEN 5.0
                    WHEN 'fine' THEN 4.0
                    WHEN 'standard' THEN 3.0
                    WHEN 'poor' THEN 2.0
                    WHEN 'terrible' THEN 1.0
                    ELSE 3.0
                END
            ),
            2
        ) AS avg_equipment_quality,
        JSON_GROUP_ARRAY(se.equipment_id) AS equipment_ids
    FROM
        Squad_Equipment se
        JOIN Equipment e ON e.equipment_id = se.equipment_id
    GROUP BY
        se.squad_id
),
training_stats AS (
    SELECT
        squad_id,
        COUNT(*) AS total_training_sessions,
        ROUND(AVG(effectiveness) / 100.0, 2) AS avg_training_effectiveness,
        JSON_GROUP_ARRAY(schedule_id) AS training_ids
    FROM
        Squad_Training
    GROUP BY
        squad_id
),
combat_skill_stats AS (
    SELECT
        sm.squad_id,
        ROUND(AVG(ds.level), 2) AS avg_combat_skill_improvement
    FROM
        Squad_Members sm
        JOIN Dwarf_Skills ds ON ds.dwarf_id = sm.dwarf_id
        AND ds.skill_id = 3
    GROUP BY
        sm.squad_id
),
training_battle_corr AS (
    SELECT
        st.squad_id,
        ROUND(
            (
                COUNT(*) * SUM(
                    CAST(st.effectiveness AS REAL) * CASE
                        sb.outcome
                        WHEN 'victory' THEN 1.0
                        ELSE 0.0
                    END
                ) - SUM(CAST(st.effectiveness AS REAL)) * SUM(
                    CASE
                        sb.outcome
                        WHEN 'victory' THEN 1.0
                        ELSE 0.0
                    END
                )
            ) / NULLIF(
                SQRT(
                    ABS(
                        (
                            COUNT(*) * SUM(
                                CAST(st.effectiveness * st.effectiveness AS REAL)
                            ) - SUM(CAST(st.effectiveness AS REAL)) * SUM(CAST(st.effectiveness AS REAL))
                        ) * (
                            COUNT(*) * SUM(
                                CASE
                                    sb.outcome
                                    WHEN 'victory' THEN 1.0
                                    ELSE 0.0
                                END * CASE
                                    sb.outcome
                                    WHEN 'victory' THEN 1.0
                                    ELSE 0.0
                                END
                            ) - SUM(
                                CASE
                                    sb.outcome
                                    WHEN 'victory' THEN 1.0
                                    ELSE 0.0
                                END
                            ) * SUM(
                                CASE
                                    sb.outcome
                                    WHEN 'victory' THEN 1.0
                                    ELSE 0.0
                                END
                            )
                        )
                    )
                ),
                0
            ),
            2
        ) AS training_battle_correlation
    FROM
        Squad_Training st
        JOIN Squad_Battles sb ON sb.squad_id = st.squad_id
        AND sb.date >= st.date
    GROUP BY
        st.squad_id
)
SELECT
    sq.squad_id,
    sq.name AS squad_name,
    sq.formation_type,
    d.name AS leader_name,
    COALESCE(bs.total_battles, 0) AS total_battles,
    COALESCE(bs.victories, 0) AS victories,
    COALESCE(bs.victory_percentage, 0.0) AS victory_percentage,
    ROUND(
        CAST(COALESCE(bs.total_casualties, 0) AS REAL) / NULLIF(ms.total_members_ever, 0) * 100,
        2
    ) AS casualty_rate,
    COALESCE(bs.casualty_exchange_ratio, 0.0) AS casualty_exchange_ratio,
    COALESCE(ms.current_members, 0) AS current_members,
    COALESCE(ms.total_members_ever, 0) AS total_members_ever,
    COALESCE(ms.retention_rate, 0.0) AS retention_rate,
    COALESCE(eq.avg_equipment_quality, 0.0) AS avg_equipment_quality,
    COALESCE(ts.total_training_sessions, 0) AS total_training_sessions,
    COALESCE(ts.avg_training_effectiveness, 0.0) AS avg_training_effectiveness,
    COALESCE(tbc.training_battle_correlation, 0.0) AS training_battle_correlation,
    COALESCE(cs.avg_combat_skill_improvement, 0.0) AS avg_combat_skill_improvement,
    ROUND(
        COALESCE(bs.victory_percentage, 0.0) / 100.0 * 0.4 + COALESCE(ts.avg_training_effectiveness, 0.0) * 0.3 + COALESCE(ms.retention_rate, 0.0) / 100.0 * 0.2 + COALESCE(eq.avg_equipment_quality, 0.0) / 10.0 * 0.1,
        3
    ) AS overall_effectiveness_score,
    JSON_OBJECT(
        'member_ids',
        JSON(COALESCE(ms.member_ids, '[]')),
        'equipment_ids',
        JSON(COALESCE(eq.equipment_ids, '[]')),
        'battle_report_ids',
        JSON(COALESCE(bs.battle_report_ids, '[]')),
        'training_ids',
        JSON(COALESCE(ts.training_ids, '[]'))
    ) AS related_entities
FROM
    Military_Squads sq
    LEFT JOIN Dwarves d ON d.dwarf_id = sq.leader_id
    LEFT JOIN battle_stats bs ON bs.squad_id = sq.squad_id
    LEFT JOIN member_stats ms ON ms.squad_id = sq.squad_id
    LEFT JOIN equipment_stats eq ON eq.squad_id = sq.squad_id
    LEFT JOIN training_stats ts ON ts.squad_id = sq.squad_id
    LEFT JOIN combat_skill_stats cs ON cs.squad_id = sq.squad_id
    LEFT JOIN training_battle_corr tbc ON tbc.squad_id = sq.squad_id
ORDER BY
    overall_effectiveness_score DESC;
