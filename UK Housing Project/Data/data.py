# This is to create a sample of the full dataset due to the csv being too large
# The full dataset is 262mb and contains +1500000 rows, whilst the sample is 24mb and contains 150000 rows

import pandas as pd

df = pd.read_csv("property_data_all.csv")
df_sample = df.sample(n=150000, random_state=1)  
df_sample.to_csv("property_data.csv", index=False)