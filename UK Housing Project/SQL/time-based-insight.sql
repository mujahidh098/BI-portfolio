-- Time Details

WITH MonthlySales AS (
    SELECT
        YEAR(Date_of_Transfer) AS Year,
        MONTH(Date_of_Transfer) AS Month,
        MONTHNAME(Date_of_Transfer) AS MonthName,
        COUNT(Transaction_ID) AS Sales,
        ROW_NUMBER() OVER (PARTITION BY YEAR(Date_of_Transfer) ORDER BY COUNT(Transaction_ID) DESC) AS MonthRank
    FROM 
        PropertyData pd 
    GROUP BY 
        YEAR(Date_of_Transfer), MONTH(Date_of_Transfer), MONTHNAME(Date_of_Transfer)
),
SalesData AS (
    SELECT
        YEAR(Date_of_Transfer) AS Year,
        COUNT(Transaction_ID) AS Sales,
        COUNT(CASE WHEN Old_New = 'Y' THEN 1 END) AS New,
        COUNT(CASE WHEN Old_New = 'N' THEN 1 END) AS Existing,
        ROUND(AVG(price), 2) AS AvgPrice,
        MAX(price) AS MaxPrice,
        MIN(price) AS MinPrice
    FROM 
        PropertyData pd 
    GROUP BY 
        YEAR(Date_of_Transfer)
)
SELECT
    sd.Year,
    sd.Sales,
    sd.New,
    sd.Existing,
    sd.MinPrice,
    sd.AvgPrice,
    sd.MaxPrice,
    ROUND(
        (sd.Sales - LAG(sd.Sales) OVER (ORDER BY sd.Year)) / 
        NULLIF(LAG(sd.Sales) OVER (ORDER BY sd.Year), 0) * 100, 
        2
    ) AS YoYGrowth,
    ms.MonthName AS TopMonth,
    ms.Sales AS TopMonthSales
FROM 
    SalesData sd
LEFT JOIN 
    MonthlySales ms ON sd.Year = ms.Year AND ms.MonthRank = 1
ORDER BY 
    sd.Year;


-- Most Sales per Month

SELECT
    MONTHNAME(Date_of_Transfer) AS Month,
    COUNT(Transaction_ID) AS Sales
FROM 
    PropertyData pd 
GROUP BY 
    MONTH(Date_of_Transfer), MONTHNAME(Date_of_Transfer)
ORDER BY 
    MONTH(Date_of_Transfer) ASC;
