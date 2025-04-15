import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# SQL Connection
engine = create_engine('mysql+pymysql://username:password@localhost/databasename')

# Load Property Sales Summary
query = """
SELECT
    YEAR(Date_of_Transfer) AS Year,
    COUNT(Transaction_ID) AS Sales,
    ROUND(AVG(price), 2) AS AvgPrice
FROM 
    PropertyData
GROUP BY 
    YEAR(Date_of_Transfer)
ORDER BY 
    YEAR(Date_of_Transfer);
"""

sales_df = pd.read_sql(query, engine)

# Simulate Macroeconomic Variables (Realistic Trends)
years = list(range(1998, 2031))
np.random.seed(42)

inflation = np.clip(np.random.normal(2.5, 1, len(years)), 1.5, 6.5)
interest_rates = np.clip(np.random.normal(3.5, 1.5, len(years)), 0.5, 7)
unemployment = np.clip(np.random.normal(5.5, 1.2, len(years)), 3.5, 8.5)
property_taxes = np.clip(np.random.normal(1.3, 0.2, len(years)), 1.0, 2.0)

macro_df = pd.DataFrame({
    'Year': years,
    'Inflation': inflation,
    'Interest_Rate': interest_rates,
    'Unemployment_Rate': unemployment,
    'Property_Tax_Rate': property_taxes
})

# Merge Macro Data with Sales
full_df = pd.merge(sales_df, macro_df, how='right', on='Year')

# Fill missing past sales with rolling averages
full_df['Sales'] = full_df['Sales'].interpolate(method='linear')

# Prepare for Prophet
prophet_df = full_df[['Year', 'Sales', 'Inflation', 'Interest_Rate', 'Unemployment_Rate', 'Property_Tax_Rate']].copy()
prophet_df.rename(columns={'Year': 'ds', 'Sales': 'y'}, inplace=True)
prophet_df['ds'] = pd.to_datetime(prophet_df['ds'], format='%Y')

# Fit Prophet Model with Regressors
model = Prophet()
for col in ['Inflation', 'Interest_Rate', 'Unemployment_Rate', 'Property_Tax_Rate']:
    model.add_regressor(col)

model.fit(prophet_df)

# Future Dataframe
future = model.make_future_dataframe(periods=7, freq='Y')  # 7 more years till 2030

# Add macro forecasts (simulate realistic future macro trends)
future_macros = macro_df.loc[macro_df['Year'] >= 2024].reset_index(drop=True)
for col in ['Inflation', 'Interest_Rate', 'Unemployment_Rate', 'Property_Tax_Rate']:
    future[col] = list(full_df[col]) + list(future_macros[col].values)

# Forecast
forecast = model.predict(future)

# Visualization — Actual + Forecasted Sales
plt.figure(figsize=(14, 7))
plt.plot(prophet_df['ds'], prophet_df['y'], label='Actual Sales', marker='o')
plt.plot(forecast['ds'], forecast['yhat'], label='Forecasted Sales', linestyle='--', color='orange')
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='orange', alpha=0.3)
plt.title('UK Housing Sales Forecast (1998–2030)')
plt.xlabel('Year')
plt.ylabel('Number of Transactions')
plt.legend()
plt.grid(True)
plt.show()

# Correlation Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(full_df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Between Housing Sales and Macroeconomic Variables')
plt.show()