-- Property Type

SELECT
    CASE
        WHEN Property_Type = 'F' THEN 'Flat'
        WHEN Property_Type = 'T' THEN 'Terraced'
        WHEN Property_Type = 'D' THEN 'Detached'
        WHEN Property_Type = 'S' THEN 'Semi-Detached'
        WHEN Property_Type = 'O' THEN 'Other'
        ELSE 'Unknown'
    END AS PropertyTypeName,
    COUNT(Transaction_ID) AS Sales,
    MIN(price) AS MinPrice,
    ROUND(AVG(price), 2) AS AvgPrice,
    MAX(price) AS MaxPrice
FROM 
    PropertyData pd 
GROUP BY 
    Property_Type;