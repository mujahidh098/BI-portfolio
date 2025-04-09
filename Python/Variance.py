import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# DB Connection
try:
    engine = create_engine('mysql+pymysql://root:***********@localhost/sample')
    connection = engine.connect()
    print("Connection successful.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    connection = None

if connection:
    query = """
    SELECT
        DAY(createdAt) AS Day,
        MONTH(createdAt) AS Month,
        YEAR(createdAt) AS Year,
        SUM(total) AS Sales
    FROM 
        Orders o
    WHERE 
        o.status = 'COMPLETED' AND
        MONTH(createdAt) = 2 AND
        YEAR(createdAt) = 2025
    GROUP BY 
        DAY(createdAt), MONTH(createdAt), YEAR(createdAt)
    ORDER BY
        YEAR(createdAt), MONTH(createdAt), DAY(createdAt);
    """

    print("Executing query:\n", query)

    try:
        df = pd.read_sql(query, connection)
        connection.close()
        print("Data loaded successfully.")

        # Build full date range for February 2025
        all_days = pd.date_range(start='2025-02-01', end='2025-02-28', freq='D')
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        df = df.set_index('Date').reindex(all_days).fillna(0).reset_index()
        df.rename(columns={'index': 'Date'}, inplace=True)

        # Fixing column order and types
        df['Day'] = df['Date'].dt.day
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        df['Sales'] = df['Sales'].astype(float)

        # Feature Engineering
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        df['DayOfMonth'] = df['Date'].dt.day
        df['Month'] = df['Date'].dt.month

        # Model Prep
        X = df[['DayOfWeek', 'DayOfMonth', 'Month']]
        y = df['Sales']

        # Train/Test Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Random Forest Model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X)

        # Evaluation
        mse = mean_squared_error(y, predictions)
        print(f"Mean Squared Error: {mse:.2f}")

        # Final dataframe for plotting
        results_df = df[['Date', 'Sales']].copy()
        results_df['Predicted Sales'] = predictions
        results_df['Variance (%)'] = (results_df['Sales'] - results_df['Predicted Sales']) / results_df['Sales'].replace(0, 1) * 100

        # Plot 1: Actual vs Predicted Sales
        plt.figure(figsize=(12, 6))
        plt.plot(results_df['Date'], results_df['Sales'], label='Actual Sales', marker='o')
        plt.plot(results_df['Date'], results_df['Predicted Sales'], label='Predicted Sales', marker='x')

        for i in range(len(results_df)):
            plt.text(results_df['Date'].iloc[i], results_df['Sales'].iloc[i],
                     f"{results_df['Sales'].iloc[i]:.2f}", fontsize=8, ha='right', va='bottom')
            plt.text(results_df['Date'].iloc[i], results_df['Predicted Sales'].iloc[i],
                     f"{results_df['Predicted Sales'].iloc[i]:.2f}", fontsize=8, ha='right', va='top')

        plt.title("Actual vs Predicted Sales for February 2025")
        plt.xlabel("Date")
        plt.ylabel("Sales Amount")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

        # Plot 2: Variance Bar Chart
        plt.figure(figsize=(12, 6))
        plt.bar(results_df['Date'], results_df['Variance (%)'],
                color=['green' if x >= 0 else 'red' for x in results_df['Variance (%)']])

        for i in range(len(results_df)):
            plt.text(results_df['Date'].iloc[i], results_df['Variance (%)'].iloc[i],
                     f"{results_df['Variance (%)'].iloc[i]:.2f}%", fontsize=8, ha='center', va='bottom')

        plt.title("Variance between Actual and Predicted Sales for February 2025")
        plt.xlabel("Date")
        plt.ylabel("Variance (%)")
        plt.axhline(0, color='black', linewidth=0.8)
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error executing query: {e}")