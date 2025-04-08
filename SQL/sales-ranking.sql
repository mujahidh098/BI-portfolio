-- Sales Ranking

SELECT
    name,
    order_count,
    total_sales,
    RANK() OVER (ORDER BY order_count DESC) AS `rank`
FROM (
    SELECT
        mi.name AS name,
        COUNT(omi.id) AS order_count,
        SUM(omi.total) AS total_sales
    FROM OrderMenuItems omi
    INNER JOIN MenuItems mi ON omi.itemId = mi.id
    INNER JOIN Orders o ON omi.orderId = o.id
    WHERE o.status = 'COMPLETED'
    GROUP BY mi.name
) AS item_stats;