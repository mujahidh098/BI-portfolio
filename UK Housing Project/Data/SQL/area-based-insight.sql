-- County Details

WITH CountyYearSales AS (
    SELECT
        County,
        YEAR(Date_of_Transfer) AS Year,
        COUNT(Transaction_ID) AS Sales,
        ROW_NUMBER() OVER (PARTITION BY County ORDER BY COUNT(Transaction_ID) DESC) AS rn
    FROM 
        PropertyData
    GROUP BY 
        County, YEAR(Date_of_Transfer)
)
, BestCountyYears AS (
    SELECT
        County,
        Year AS BestYear
    FROM 
        CountyYearSales
    WHERE
        rn = 1
)
SELECT
    pd.County,
    COUNT(Transaction_ID) AS Sales,
    MIN(price) AS MinPrice,
    ROUND(AVG(price), 2) AS AvgPrice,
    MAX(price) AS MaxPrice,
    bc.BestYear
FROM 
    PropertyData pd
LEFT JOIN 
    BestCountyYears bc ON pd.County = bc.County
GROUP BY 
    pd.County, bc.BestYear;