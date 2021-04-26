import pandas as pd

humor_data = pd.read_csv('files/dev.csv')

print("\n----- Head -----")
print(humor_data.head())

print("\n----- Describe ------")
print(humor_data.describe())