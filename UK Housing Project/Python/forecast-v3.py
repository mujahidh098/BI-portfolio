import pandas as pd
import mysql.connector
from prophet import Prophet
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from datetime import datetime

# Connect to your MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)

# Pull sales data
query = """
    SELECT 
        Date_of_Transfer AS date,
        COUNT(Transaction_ID) AS sales,
        ROUND(AVG(price), 2) AS avg_price
    FROM 
        PropertyData
    GROUP BY 
        Date_of_Transfer
    ORDER BY 
        Date_of_Transfer
"""

df = pd.read_sql(query, conn)
conn.close()

# Preprocess
df['date'] = pd.to_datetime(df['date'])
df_daily = df.groupby('date').agg({'sales': 'sum', 'avg_price': 'mean'}).reset_index()

# Create synthetic macroeconomic variables (for now)
np.random.seed(42)
df_daily['inflation'] = np.random.normal(2.5, 0.5, len(df_daily))  # % inflation
df_daily['unemployment'] = np.random.normal(4.5, 0.3, len(df_daily))  # % unemployment
df_daily['property_tax_index'] = np.random.normal(100, 5, len(df_daily))  # base 100 index
df_daily['area_desirability_index'] = np.random.normal(70, 15, len(df_daily))  # subjective desirability

# Prophet requires 'ds' and 'y'
df_prophet = df_daily.rename(columns={'date': 'ds', 'sales': 'y'})

# Build Prophet model
model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
model.add_regressor('inflation')
model.add_regressor('unemployment')
model.add_regressor('property_tax_index')
model.add_regressor('area_desirability_index')

# Fit model
model.fit(df_prophet[['ds', 'y', 'inflation', 'unemployment', 'property_tax_index', 'area_desirability_index']])

# Create future dataframe to 2030
future = model.make_future_dataframe(periods=365*6)  # 6 years from 2025
future['inflation'] = np.random.normal(2.3, 0.5, len(future))
future['unemployment'] = np.random.normal(4.2, 0.3, len(future))
future['property_tax_index'] = np.random.normal(105, 5, len(future))
future['area_desirability_index'] = np.random.normal(72, 12, len(future))

# Predict
forecast = model.predict(future)

# Compare 2024 actual vs predicted (if you have it — else placeholder)
actual_2024 = df_prophet[(df_prophet['ds'] >= '2024-01-01') & (df_prophet['ds'] < '2025-01-01')]

forecast_2024 = forecast[(forecast['ds'] >= '2024-01-01') & (forecast['ds'] < '2025-01-01')]

# Error calculation placeholder
if not actual_2024.empty:
    merged_2024 = pd.merge(actual_2024, forecast_2024, on='ds')
    merged_2024['error'] = abs(merged_2024['y'] - merged_2024['yhat']) / merged_2024['y'] * 100
    accuracy_2024 = 100 - merged_2024['error'].mean()
    print(f"📊 2024 Forecast Accuracy: {accuracy_2024:.2f}%")

# Matplotlib Forecast Plot
plt.figure(figsize=(14, 6))
plt.plot(df_prophet['ds'], df_prophet['y'], label='Actual Sales')
plt.plot(forecast['ds'], forecast['yhat'], label='Forecast')
plt.title('UK Property Sales Forecast')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.show()

# Plotly Interactive Dashboard
fig = px.line(forecast, x='ds', y=['yhat', 'yhat_lower', 'yhat_upper'],
              labels={'value': 'Sales', 'ds': 'Date'},
              title='Interactive UK Housing Sales Forecast (1998–2030)')
fig.show()