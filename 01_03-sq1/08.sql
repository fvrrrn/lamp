WITH civ_trade AS (
    SELECT
        c.caravan_id,
        c.civilization_type,
        c.arrival_date,
        COALESCE(
            (
                SELECT
                    SUM(tt.value)
                FROM
                    Trade_Transactions tt
                WHERE
                    tt.caravan_id = c.caravan_id
            ),
            0
        ) AS caravan_value,
        COALESCE(
            (
                SELECT
                    SUM(
                        CASE
                            WHEN tt.balance_direction = 'export' THEN tt.value
                            ELSE - tt.value
                        END
                    )
                FROM
                    Trade_Transactions tt
                WHERE
                    tt.caravan_id = c.caravan_id
            ),
            0
        ) AS caravan_balance,
        COALESCE(
            (
                SELECT
                    SUM(de.relationship_change)
                FROM
                    Diplomatic_Events de
                WHERE
                    de.caravan_id = c.caravan_id
            ),
            0
        ) AS relationship_change
    FROM
        Caravans c
),
civ_stats AS (
    SELECT
        civilization_type,
        COUNT(caravan_id) AS total_caravans,
        SUM(caravan_value) AS total_trade_value,
        SUM(caravan_balance) AS trade_balance,
        ROUND(
            (
                COUNT(*) * SUM(
                    CAST(caravan_value AS REAL) * relationship_change
                ) - SUM(CAST(caravan_value AS REAL)) * SUM(relationship_change)
            ) / NULLIF(
                SQRT(
                    ABS(
                        (
                            COUNT(*) * SUM(CAST(caravan_value AS REAL) * caravan_value) - SUM(CAST(caravan_value AS REAL)) * SUM(caravan_value)
                        ) * (
                            COUNT(*) * SUM(
                                CAST(relationship_change AS REAL) * relationship_change
                            ) - SUM(CAST(relationship_change AS REAL)) * SUM(relationship_change)
                        )
                    )
                ),
                0
            ),
            4
        ) AS diplomatic_correlation,
        JSON_GROUP_ARRAY(caravan_id) AS caravan_ids
    FROM
        civ_trade
    GROUP BY
        civilization_type
),
import_deps AS (
    SELECT
        cg.material_type,
        ROUND(
            CAST(SUM(cg.value * cg.quantity) AS REAL) / COUNT(DISTINCT cg.caravan_id),
            1
        ) AS dependency_score,
        SUM(cg.quantity) AS total_imported,
        COUNT(DISTINCT cg.caravan_id) AS import_diversity,
        JSON_GROUP_ARRAY(cg.goods_id) AS resource_ids
    FROM
        Caravan_Goods cg
    WHERE
        cg.type = 'import'
        AND cg.material_type IS NOT NULL
    GROUP BY
        cg.material_type
),
export_eff AS (
    SELECT
        w.type AS workshop_type,
        p.type AS product_type,
        ROUND(
            CAST(COUNT(cg.goods_id) AS REAL) / NULLIF(COUNT(p.product_id), 0) * 100,
            1
        ) AS export_ratio,
        ROUND(
            AVG(CAST(cg.value AS REAL) / NULLIF(p.value, 0)),
            2
        ) AS avg_markup
    FROM
        Workshops w
        JOIN Products p ON p.workshop_id = w.workshop_id
        LEFT JOIN Caravan_Goods cg ON cg.original_product_id = p.product_id
    GROUP BY
        w.type,
        p.type
),
trade_timeline AS (
    SELECT
        CAST(SUBSTR(tt.date, 1, 3) AS INTEGER) AS year,
        (CAST(SUBSTR(tt.date, 5, 2) AS INTEGER) - 1) / 3 + 1 AS quarter,
        SUM(tt.value) AS quarterly_value,
        SUM(
            CASE
                WHEN tt.balance_direction = 'export' THEN tt.value
                ELSE - tt.value
            END
        ) AS quarterly_balance,
        COUNT(DISTINCT c.civilization_type) AS trade_diversity
    FROM
        Trade_Transactions tt
        JOIN Caravans c ON c.caravan_id = tt.caravan_id
    GROUP BY
        year,
        quarter
)
SELECT
    JSON_OBJECT(
        'total_trading_partners',
        (
            SELECT
                COUNT(DISTINCT civilization_type)
            FROM
                Caravans
        ),
        'all_time_trade_value',
        (
            SELECT
                COALESCE(SUM(value), 0)
            FROM
                Trade_Transactions
        ),
        'all_time_trade_balance',
        (
            SELECT
                COALESCE(
                    SUM(
                        CASE
                            WHEN balance_direction = 'export' THEN value
                            ELSE - value
                        END
                    ),
                    0
                )
            FROM
                Trade_Transactions
        ),
        'civilization_data',
        JSON_OBJECT(
            'civilization_trade_data',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'civilization_type',
                                    cs.civilization_type,
                                    'total_caravans',
                                    cs.total_caravans,
                                    'total_trade_value',
                                    cs.total_trade_value,
                                    'trade_balance',
                                    cs.trade_balance,
                                    'trade_relationship',
                                    CASE
                                        WHEN cs.trade_balance >= 0 THEN 'Favorable'
                                        ELSE 'Unfavorable'
                                    END,
                                    'diplomatic_correlation',
                                    cs.diplomatic_correlation,
                                    'caravan_ids',
                                    JSON(cs.caravan_ids)
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    civ_stats
                                ORDER BY
                                    total_trade_value DESC
                            ) cs
                    ),
                    '[]'
                )
            )
        ),
        'critical_import_dependencies',
        JSON_OBJECT(
            'resource_dependency',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'material_type',
                                    id.material_type,
                                    'dependency_score',
                                    id.dependency_score,
                                    'total_imported',
                                    id.total_imported,
                                    'import_diversity',
                                    id.import_diversity,
                                    'resource_ids',
                                    JSON(id.resource_ids)
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    import_deps
                                ORDER BY
                                    dependency_score DESC
                            ) id
                    ),
                    '[]'
                )
            )
        ),
        'export_effectiveness',
        JSON_OBJECT(
            'export_effectiveness',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'workshop_type',
                                    ee.workshop_type,
                                    'product_type',
                                    ee.product_type,
                                    'export_ratio',
                                    ee.export_ratio,
                                    'avg_markup',
                                    ee.avg_markup,
                                    'workshop_ids',
                                    JSON(
                                        (
                                            SELECT
                                                JSON_GROUP_ARRAY(workshop_id)
                                            FROM
                                                Workshops
                                            WHERE
                                                TYPE = ee.workshop_type
                                        )
                                    )
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    export_eff
                                ORDER BY
                                    export_ratio DESC
                            ) ee
                    ),
                    '[]'
                )
            )
        ),
        'trade_timeline',
        JSON_OBJECT(
            'trade_growth',
            JSON(
                COALESCE(
                    (
                        SELECT
                            JSON_GROUP_ARRAY(
                                JSON_OBJECT(
                                    'year',
                                    tl.year,
                                    'quarter',
                                    tl.quarter,
                                    'quarterly_value',
                                    tl.quarterly_value,
                                    'quarterly_balance',
                                    tl.quarterly_balance,
                                    'trade_diversity',
                                    tl.trade_diversity
                                )
                            )
                        FROM
                            (
                                SELECT
                                    *
                                FROM
                                    trade_timeline
                                ORDER BY
                                    year,
                                    quarter
                            ) tl
                    ),
                    '[]'
                )
            )
        )
    ) AS trade_analysis;
