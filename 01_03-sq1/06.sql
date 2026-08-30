WITH production_events AS (
    SELECT
        wp.workshop_id,
        wp.production_date,
        wp.quantity,
        p.value,
        SUBSTR(wp.production_date, 1, 3) || '-Q' || CAST(
            (
                CAST(SUBSTR(wp.production_date, 5, 2) AS INTEGER) - 1
            ) / 3 + 1 AS TEXT
        ) AS year_quarter,
        LAG(wp.production_date) OVER (
            PARTITION BY wp.workshop_id
            ORDER BY
                wp.production_date
        ) AS prev_production_date
    FROM
        Workshop_Products wp
        JOIN Products p ON p.product_id = wp.product_id
),
production_stats AS (
    SELECT
        workshop_id,
        SUM(quantity) AS total_quantity_produced,
        SUM(quantity * value) AS total_production_value,
        COUNT(DISTINCT year_quarter) AS active_quarters,
        CASE
            WHEN MIN(production_date) = MAX(production_date) THEN 1
            ELSE (
                CAST(SUBSTR(MAX(production_date), 1, 3) AS INTEGER) * 365 + CAST(SUBSTR(MAX(production_date), 5, 2) AS INTEGER) * 30 + CAST(SUBSTR(MAX(production_date), 8, 2) AS INTEGER)
            ) - (
                CAST(SUBSTR(MIN(production_date), 1, 3) AS INTEGER) * 365 + CAST(SUBSTR(MIN(production_date), 5, 2) AS INTEGER) * 30 + CAST(SUBSTR(MIN(production_date), 8, 2) AS INTEGER)
            ) + 1
        END AS span_days,
        (
            CAST(SUBSTR(MAX(production_date), 1, 3) AS INTEGER) - CAST(SUBSTR(MIN(production_date), 1, 3) AS INTEGER)
        ) * 4 + (
            CAST(SUBSTR(MAX(production_date), 5, 2) AS INTEGER) - 1
        ) / 3 - (
            CAST(SUBSTR(MIN(production_date), 5, 2) AS INTEGER) - 1
        ) / 3 + 1 AS span_quarters,
        SUM(
            CASE
                WHEN prev_production_date IS NULL THEN 0
                ELSE CAST(SUBSTR(production_date, 1, 3) AS INTEGER) * 365 + CAST(SUBSTR(production_date, 5, 2) AS INTEGER) * 30 + CAST(SUBSTR(production_date, 8, 2) AS INTEGER) - (
                    CAST(SUBSTR(prev_production_date, 1, 3) AS INTEGER) * 365 + CAST(SUBSTR(prev_production_date, 5, 2) AS INTEGER) * 30 + CAST(SUBSTR(prev_production_date, 8, 2) AS INTEGER)
                ) - 1
            END
        ) AS total_idle_days
    FROM
        production_events
    GROUP BY
        workshop_id
),
material_stats AS (
    SELECT
        workshop_id,
        SUM(
            CASE
                WHEN is_input = 1 THEN quantity
                ELSE 0
            END
        ) AS total_input_qty
    FROM
        Workshop_Materials
    GROUP BY
        workshop_id
),
craftsdwarf_stats AS (
    SELECT
        wc.workshop_id,
        COUNT(DISTINCT wc.dwarf_id) AS num_craftsdwarves,
        ROUND(AVG(COALESCE(ds_avg.avg_skill, 0)), 2) AS avg_craftsdwarf_skill,
        JSON_GROUP_ARRAY(wc.dwarf_id) AS craftsdwarf_ids
    FROM
        Workshop_Craftsdwarves wc
        LEFT JOIN (
            SELECT
                dwarf_id,
                AVG(LEVEL) AS avg_skill
            FROM
                Dwarf_Skills
            GROUP BY
                dwarf_id
        ) ds_avg ON ds_avg.dwarf_id = wc.dwarf_id
    GROUP BY
        wc.workshop_id
),
skill_quality_corr AS (
    SELECT
        p.workshop_id,
        ROUND(
            (
                COUNT(*) * SUM(ds_avg.avg_skill * qn.quality_numeric) - SUM(ds_avg.avg_skill) * SUM(qn.quality_numeric)
            ) / NULLIF(
                SQRT(
                    ABS(
                        (
                            COUNT(*) * SUM(ds_avg.avg_skill * ds_avg.avg_skill) - SUM(ds_avg.avg_skill) * SUM(ds_avg.avg_skill)
                        ) * (
                            COUNT(*) * SUM(qn.quality_numeric * qn.quality_numeric) - SUM(qn.quality_numeric) * SUM(qn.quality_numeric)
                        )
                    )
                ),
                0
            ),
            4
        ) AS skill_quality_correlation
    FROM
        Products p
        JOIN (
            SELECT
                dwarf_id,
                CAST(AVG(LEVEL) AS REAL) AS avg_skill
            FROM
                Dwarf_Skills
            GROUP BY
                dwarf_id
        ) ds_avg ON ds_avg.dwarf_id = p.created_by
        JOIN (
            SELECT
                'legendary' AS quality_name,
                8.0 AS quality_numeric
            UNION
            ALL
            SELECT
                'masterwork',
                7.0
            UNION
            ALL
            SELECT
                'exceptional',
                6.0
            UNION
            ALL
            SELECT
                'superior',
                5.0
            UNION
            ALL
            SELECT
                'fine',
                4.0
            UNION
            ALL
            SELECT
                'standard',
                3.0
            UNION
            ALL
            SELECT
                'poor',
                2.0
            UNION
            ALL
            SELECT
                'terrible',
                1.0
        ) qn ON LOWER(p.quality) = qn.quality_name
    WHERE
        p.workshop_id IS NOT NULL
    GROUP BY
        p.workshop_id
)
SELECT
    w.workshop_id,
    w.name AS workshop_name,
    w.type AS workshop_type,
    COALESCE(cs.num_craftsdwarves, 0) AS num_craftsdwarves,
    COALESCE(ps.total_quantity_produced, 0) AS total_quantity_produced,
    COALESCE(ps.total_production_value, 0) AS total_production_value,
    ROUND(
        CAST(COALESCE(ps.total_quantity_produced, 0) AS REAL) / NULLIF(
            ps.span_days - COALESCE(ps.total_idle_days, 0),
            0
        ),
        2
    ) AS daily_production_rate,
    ROUND(
        CAST(COALESCE(ps.total_production_value, 0) AS REAL) / NULLIF(ms.total_input_qty, 0),
        2
    ) AS value_per_material_unit,
    ROUND(
        CAST(COALESCE(ps.active_quarters, 0) AS REAL) / NULLIF(ps.span_quarters, 0) * 100,
        2
    ) AS workshop_utilization_percent,
    ROUND(
        CAST(COALESCE(ps.total_quantity_produced, 0) AS REAL) / NULLIF(ms.total_input_qty, 0),
        4
    ) AS material_conversion_ratio,
    COALESCE(cs.avg_craftsdwarf_skill, 0) AS average_craftsdwarf_skill,
    sqc.skill_quality_correlation,
    JSON_OBJECT(
        'craftsdwarf_ids',
        JSON(COALESCE(cs.craftsdwarf_ids, '[]')),
        'product_ids',
        JSON(
            COALESCE(
                (
                    SELECT
                        JSON_GROUP_ARRAY(product_id)
                    FROM
                        Workshop_Products
                    WHERE
                        workshop_id = w.workshop_id
                ),
                '[]'
            )
        ),
        'material_ids',
        JSON(
            COALESCE(
                (
                    SELECT
                        JSON_GROUP_ARRAY(material_id)
                    FROM
                        Workshop_Materials
                    WHERE
                        workshop_id = w.workshop_id
                        AND is_input = 1
                ),
                '[]'
            )
        ),
        'project_ids',
        JSON(
            COALESCE(
                (
                    SELECT
                        JSON_GROUP_ARRAY(project_id)
                    FROM
                        Projects
                    WHERE
                        workshop_id = w.workshop_id
                ),
                '[]'
            )
        )
    ) AS related_entities
FROM
    Workshops w
    LEFT JOIN production_stats ps ON ps.workshop_id = w.workshop_id
    LEFT JOIN material_stats ms ON ms.workshop_id = w.workshop_id
    LEFT JOIN craftsdwarf_stats cs ON cs.workshop_id = w.workshop_id
    LEFT JOIN skill_quality_corr sqc ON sqc.workshop_id = w.workshop_id
ORDER BY
    total_production_value DESC;
