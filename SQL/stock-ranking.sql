-- Most Expensive Stock Items

SELECT
    name,
    stock_count,
    total_purchases,
    RANK() OVER (ORDER BY total_purchases DESC) AS `rank`
FROM (
    SELECT
        st.stockItemStockCode AS name,
        COUNT(st.id) AS stock_count,
        SUM(transactionCost) AS total_purchases
    FROM StockTransactions st 
    GROUP BY st.stockItemStockCode
) AS item_stats;