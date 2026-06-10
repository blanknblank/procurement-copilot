import pandas as pd

df = pd.read_csv('data/procurement_transactions.csv')

print(df.shape)

print(df['category'].value_counts())

print(df.groupby('supplier')['spend'].sum().sort_values(ascending=False).head())

print(df.groupby('category')['spend'].sum())