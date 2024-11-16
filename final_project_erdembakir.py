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
plt.subplot(1, 2, 1)
# Average temperature distribution
sns.histplot(data=df, x='AverageTemperature', bins=50)
plt.title('Distribution of Average Temperatures')
plt.xlabel('Temperature')

plt.subplot(1, 2, 2)
# Temperature by year
df_yearly = df.groupby('year')['AverageTemperature'].mean().reset_index()
sns.lineplot(data=df_yearly, x='year', y='AverageTemperature')
plt.title('Average Temperature Over Years')
plt.xlabel('Year')
plt.ylabel('Average Temperature')

plt.tight_layout()
plt.show()

# Top 10 hottest 
plt.figure(figsize=(10, 6))
top_10_hottest = df.groupby('City')['AverageTemperature'].mean().sort_values(ascending=False).head(10).reset_index()
top_10_hottest['City'] = top_10_hottest['City'].apply(lambda x: f"{x} ({df.loc[df['City'] == x, 'Country'].iloc[0]})")
sns.barplot(data=top_10_hottest, x='City', y='AverageTemperature')
plt.title('Top 10 Hottest Cities (Average)')
plt.xlabel('City (Country)')
plt.ylabel('Average Temperature')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
