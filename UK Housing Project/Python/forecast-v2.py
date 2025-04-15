import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# DB Connection (update credentials as needed)
engine = create_engine("mysql+mysqlconnector://username:password@localhost:3306/your_database")

# Load property sales data
query = """
SELECT 
    YEAR(Date_of_Transfer) AS Year,
    COUNT(Transaction_ID) AS Sales,
    ROUND(AVG(Price), 2) AS AvgPrice
FROM PropertyData
GROUP BY YEAR(Date_of_Transfer)
ORDER BY Year;
"""
df = pd.read_sql(query, con=engine)

# Simulate realistic macroeconomic variables (inflation, unemployment etc.)
np.random.seed(42)
df['Inflation'] = np.linspace(1.2, 4.5, len(df)) + np.random.normal(0, 0.3, len(df))  # %
df['Unemployment'] = np.linspace(5.5, 3.8, len(df)) + np.random.normal(0, 0.2, len(df))  # %
df['MortgageRate'] = np.linspace(4.0, 6.5, len(df)) + np.random.normal(0, 0.15, len(df))  # %
df['PropertyTaxRate'] = np.linspace(1.2, 1.8, len(df)) + np.random.normal(0, 0.1, len(df))  # %
df['AreaDesirabilityIndex'] = np.linspace(60, 85, len(df)) + np.random.normal(0, 3, len(df))  # out of 100

# Prepare training data
X = df[['Year', 'Inflation', 'Unemployment', 'MortgageRate', 'PropertyTaxRate', 'AreaDesirabilityIndex']]
y = df['Sales']

# Train/Test split (up to 2023)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Model
model = XGBRegressor(objective='reg:squarederror', n_estimators=500)
model.fit(X_train, y_train)

# Validate on 2024 if exists
if 2024 in df['Year'].values:
    X_2024 = df[df['Year'] == 2024][X.columns]
    y_2024 = df[df['Year'] == 2024]['Sales']
    pred_2024 = model.predict(X_2024)
    print(f"2024 Actual Sales: {y_2024.values[0]:,.0f} | Predicted: {pred_2024[0]:,.0f}")

# Forecast 2025–2030
future_years = pd.DataFrame({
    'Year': range(2025, 2031),
    'Inflation': np.linspace(3.5, 5.0, 6) + np.random.normal(0, 0.2, 6),
    'Unemployment': np.linspace(3.8, 5.5, 6) + np.random.normal(0, 0.2, 6),
    'MortgageRate': np.linspace(5.0, 7.0, 6) + np.random.normal(0, 0.2, 6),
    'PropertyTaxRate': np.linspace(1.5, 2.0, 6) + np.random.normal(0, 0.1, 6),
    'AreaDesirabilityIndex': np.linspace(82, 90, 6) + np.random.normal(0, 2, 6)
})

future_predictions = model.predict(future_years)

# Combine actual + forecast
forecast_df = pd.concat([
    df[['Year', 'Sales']].copy(),
    pd.DataFrame({'Year': future_years['Year'], 'Sales': future_predictions})
], ignore_index=True)

# 📊 Matplotlib static visualization
plt.figure(figsize=(12, 6))
plt.plot(forecast_df['Year'], forecast_df['Sales'], marker='o')
plt.title("UK Housing Market Sales Forecast (1998-2030)")
plt.xlabel("Year")
plt.ylabel("Number of Sales")
plt.grid(True)
plt.show()

# 📈 Plotly interactive dashboard
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=forecast_df['Year'],
    y=forecast_df['Sales'],
    mode='lines+markers',
    name='Sales Forecast'
))

fig.update_layout(
    title="Interactive UK Housing Market Sales Forecast (1998-2030)",
    xaxis_title="Year",
    yaxis_title="Number of Sales",
    hovermode="x unified",
    template="plotly_white"
)

fig.show()

# 📊 Correlation heatmap
corr_df = df.drop(columns=['AvgPrice'])
corr = corr_df.corr()

fig_corr = px.imshow(corr,
                     text_auto=True,
                     color_continuous_scale='RdBu_r',
                     title="Correlation Heatmap of Macroeconomic Variables vs Sales")
fig_corr.show()

# Optional: export forecasts to CSV
forecast_df.to_csv('UK_Housing_Forecast_1998_2030.csv', index=False)