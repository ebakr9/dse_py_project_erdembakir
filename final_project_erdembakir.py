import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df = pd.read_csv("C:/Users/Erdem/Desktop/UNIMI/codingfordse/Python/dataset_weather_majorcities.csv")


print("Dataset Info:")
print(df.info())

print("Basic Statistics:")
print(df.describe())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

#onvert date column to datetime
df['dt'] = pd.to_datetime(df['dt'])
df['year'] = df['dt'].dt.year

#Basic visualizations
plt.figure(figsize=(15, 6))

#Average temperature distribution around the world
sns.histplot(data=df, x='AverageTemperature', bins=50)
plt.title('Distribution of Average Temperatures')
plt.xlabel('Temperature')
plt.show()
