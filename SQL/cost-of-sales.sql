-- Cost of Sales

WITH LatestStock AS (
    SELECT
        st.stockItemStockCode,
        MAX(DATE(st.dateOfCapture)) AS LastTransactionDate
    FROM
        StockTransactions st
    GROUP BY
        st.stockItemStockCode
),
LatestOpeningStock AS (
    SELECT
        st_sub.stockItemStockCode,
        COALESCE(SUM(st_sub.txCost), 0) AS OpeningStock
    FROM
        StockTransactions st_sub
    WHERE
        DATE(st_sub.dateOfCapture) < '2025-02-01'
    GROUP BY
        st_sub.stockItemStockCode
),
LatestClosingStock AS (
    SELECT
        st_sub.stockItemStockCode,
        COALESCE(SUM(st_sub.txCost), 0) AS ClosingStock
    FROM
        StockTransactions st_sub
    WHERE
        DATE(st_sub.dateOfCapture) <= '2025-02-28'
    GROUP BY
        st_sub.stockItemStockCode
)
SELECT *,
       COALESCE(TheoreticalGrossProfit - ActualGrossProfit, 0) AS Difference
FROM (
    SELECT
        si.stockCode AS Code,
        si.description AS Description,
        sc.name AS Category,
        COALESCE(MIN(DATE(st.dateOfCapture)), '2025-02-01') AS StartDate,
        COALESCE(MAX(DATE(st.dateOfCapture)), '2025-02-28') AS EndDate,
        COALESCE(los.OpeningStock, 0) AS OpeningStock,
        COALESCE(SUM(CASE
            WHEN st.sourceType IN ('DELIVERY_INCREASE', 'DELIVERY_DECREASE', 'CREDIT_NOTE_INCREASE', 'CREDIT_NOTE_DECREASE', 'STOCK_RETURN')
            THEN st.txCost ELSE 0 END), 0) AS Purchases,
        COALESCE(SUM(CASE
            WHEN st.sourceType IN ('TRANSFER_INCREASE', 'TRANSFER_DECREASE', 'PRODUCTION_INCREASE', 'PRODUCTION_DECREASE', 'WASTE', 'REVERSE_TRANSFER_INCREASE', 'REVERSE_TRANSFER_DECREASE', 'REVERSE_WASTE')
            THEN st.txCost ELSE 0 END), 0) AS NetStockMovement,
        COALESCE(lcs.ClosingStock, 0) AS ClosingStock,
        COALESCE(-(
            SUM(CASE WHEN st.sourceType = 'ORDER' THEN st.txCost ELSE 0 END) +
            SUM(CASE WHEN st.sourceType = 'VOID_ORDER' THEN st.txCost ELSE 0 END)
        ), 0) AS TheoreticalGrossProfit,
        COALESCE((
            COALESCE(los.OpeningStock, 0) +
            COALESCE(SUM(CASE WHEN st.sourceType IN ('DELIVERY_INCREASE', 'DELIVERY_DECREASE', 'CREDIT_NOTE_INCREASE', 'CREDIT_NOTE_DECREASE', 'STOCK_RETURN')
                THEN st.txCost ELSE 0 END), 0) +
            COALESCE(SUM(CASE WHEN st.sourceType IN ('TRANSFER_INCREASE', 'TRANSFER_DECREASE', 'PRODUCTION_INCREASE', 'PRODUCTION_DECREASE', 'WASTE', 'REVERSE_TRANSFER_INCREASE', 'REVERSE_TRANSFER_DECREASE', 'REVERSE_WASTE')
                THEN st.txCost ELSE 0 END), 0) -
            COALESCE(lcs.ClosingStock, 0)
        ), 0) AS ActualGrossProfit
    FROM
        StockItems si 
    LEFT JOIN
        StockTransactions st ON st.stockItemStockCode = si.stockCode
    LEFT JOIN
        StockCategories sc ON si.stockCategoryId = sc.externalId
    LEFT JOIN
        LatestOpeningStock los ON si.stockCode = los.stockItemStockCode
    LEFT JOIN
        LatestClosingStock lcs ON si.stockCode = lcs.stockItemStockCode
    GROUP BY
        si.stockCode, si.description, sc.name, los.OpeningStock, lcs.ClosingStock
) SubQuery;