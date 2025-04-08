import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Connect to database
try:
    engine = create_engine('mysql+pymysql://root:**********@localhost/sample')
    connection = engine.connect()
    print("Connection successful.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    connection = None

if connection:
    # SQL Query to fetch February sales data
    query = r"""
    SELECT
        DAY(createdAt) AS Day,
        SUM(total) AS Sales
    FROM 
        Orders o
    WHERE 
        o.status = 'COMPLETED' AND 
        MONTH(o.createdAt) = 2 AND 
        YEAR(o.createdAt) = 2025
    GROUP BY 
        DAY(createdAt)
    ORDER BY
        DAY(createdAt) ASC;
    """
    
    try:
        df = pd.read_sql(query, connection)
        connection.close()
        print("Data loaded successfully.")
        
        # Check if the dataframe is empty
        if df.empty:
            print("The data loaded from the database is empty.")
        else:
            print("Data preview:", df.head())  # Print the first few rows of the data

        # Add a "Date" column for ease of plotting
        df['Date'] = pd.to_datetime('2025-02-' + df['Day'].astype(str))

        # Extract Dates and create features
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        df['DayOfMonth'] = df['Date'].dt.day
        df['Month'] = df['Date'].dt.month

        # Define public holidays for 2025
        public_holidays_2025 = [
            pd.Timestamp("2025-01-01"), pd.Timestamp("2025-03-21"),
            pd.Timestamp("2025-04-18"), pd.Timestamp("2025-04-21"),
            pd.Timestamp("2025-04-27"), pd.Timestamp("2025-04-28"),
            pd.Timestamp("2025-05-01"), pd.Timestamp("2025-06-16"),
            pd.Timestamp("2025-08-09"), pd.Timestamp("2025-09-24"),
            pd.Timestamp("2025-12-16"), pd.Timestamp("2025-12-25"),
            pd.Timestamp("2025-12-26")
        ]
        public_holidays = public_holidays_2025

        # Define school holiday ranges (example)
        school_holidays = [
            (pd.Timestamp("2025-04-03"), pd.Timestamp("2025-04-19"))
        ]

        # Public and school holiday features
        df['is_public_holiday'] = df['Date'].dt.normalize().isin(public_holidays).astype(int)
        df['is_school_holiday'] = df['Date'].apply(lambda x: any(start <= x <= end for start, end in school_holidays)).astype(int)

        # Payday feature accounting for both 25th and end-of-month pay schedules
        df['is_payday'] = df['Date'].apply(lambda x: (
            x.day == 25 or 
            (x.dayofweek == 4 and x.day >= 24 and x.day <= 31) or  # Pay on Friday if 25th is a weekend
            x == (x + pd.offsets.MonthEnd(0))  # Last day of the month
        )).astype(int)

        # Check if the features (X) and target (y) are properly defined
        X = df[['DayOfWeek', 'DayOfMonth', 'Month', 'is_public_holiday', 'is_school_holiday', 'is_payday']]
        y = df['Sales']
        
        print("Features (X):", X.head())  # Print the first few rows of the features
        print("Target (y):", y.head())  # Print the first few values of the target

        if X.empty or y.empty:
            print("Features or target data is empty. Cannot train model.")
        else:
            # Train the model on historical data
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)

            # Future Date Range Prediction for March, April, and May 2025
            future_dates = pd.date_range(start='2025-03-01', end='2025-05-31', freq='D')
            future_df = pd.DataFrame(future_dates, columns=['Date'])
            future_df['DayOfWeek'] = future_df['Date'].dt.dayofweek
            future_df['DayOfMonth'] = future_df['Date'].dt.day
            future_df['Month'] = future_df['Date'].dt.month
            future_df['is_public_holiday'] = future_df['Date'].dt.normalize().isin(public_holidays).astype(int)
            future_df['is_school_holiday'] = future_df['Date'].apply(lambda x: any(start <= x <= end for start, end in school_holidays)).astype(int)
            future_df['is_payday'] = future_df['Date'].apply(lambda x: (
                x.day == 25 or 
                (x.dayofweek == 4 and x.day >= 24 and x.day <= 31) or  # Pay on Friday if 25th is a weekend
                x == (x + pd.offsets.MonthEnd(0))  # Last day of the month
            )).astype(int)

            # Predict future sales
            future_predictions = model.predict(future_df[['DayOfWeek', 'DayOfMonth', 'Month', 'is_public_holiday', 'is_school_holiday', 'is_payday']])
            future_df['Predicted Sales'] = future_predictions

            # Plot Forecast
            plt.figure(figsize=(14, 7))
            plt.plot(df['Date'], df['Sales'], label='Historical Sales (February 2025)')
            plt.plot(future_df['Date'], future_df['Predicted Sales'], label='Forecasted Sales (Mar-May 2025)', color='orange')

            # Data labels for predicted sales
            for i in range(len(future_df)):
                plt.text(future_df['Date'].iloc[i], future_df['Predicted Sales'].iloc[i],
                         f"{future_df['Predicted Sales'].iloc[i]:.2f}", 
                         fontsize=8, ha='center', color="blue")

            plt.title("Sales Forecast for March to May 2025")
            plt.xlabel("Date")
            plt.ylabel("Sales Amount")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"Error executing query: {e}")