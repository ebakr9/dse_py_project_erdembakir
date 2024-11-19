import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import geopandas as gpd
import plotly.express as px

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

# Group by year and count missing values
missing_count = df.groupby('year')['AverageTemperature'].apply(lambda x: x.isna().sum())

# Convert to a DataFrame and rename columns for clarity
missing_count_df = missing_count.reset_index(name='missing_value')

# Plotting the missing data distribution with correct axis labels
plt.figure(figsize=(12, 6))
sns.histplot(data=missing_count_df, x='year', weights='missing_value', bins=70, kde=False)

# Add labels and titles
plt.title('Distribution of Missing Data by Year', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Number of Missing Values')
plt.tight_layout()
plt.show()

#After we handle missing data in the years
# Group by country and year, and count missing values
missing_by_country = df.groupby(['Country', 'year'])['AverageTemperature'].apply(lambda x: x.isna().sum()).reset_index(name='missing_count')

#Summarize total missing data by country
missing_country_summary = missing_by_country.groupby('Country')['missing_count'].sum().reset_index()

# Sort countries by total missing values
missing_country_summary = missing_country_summary.sort_values(by='missing_count', ascending=False)
print(missing_country_summary.head(10))


# Plot total missing data by country
plt.figure(figsize=(12, 6))
sns.barplot(x='missing_count', y='Country', data=missing_country_summary.head(20))

plt.title('Top 20 Countries with the Most Missing Data', fontsize=16)
plt.xlabel('Total Missing Values')
plt.ylabel('Country')
plt.tight_layout()
plt.show()


# Filter for top countries with missing data
top_countries = missing_country_summary.head(5)['Country']

# Filter data for these countries
missing_top_countries = missing_by_country[missing_by_country['Country'].isin(top_countries)]

# Plot missing data over time for top countries
plt.figure(figsize=(12, 6))
sns.lineplot(data=missing_top_countries, x='year', y='missing_count', hue='Country')

# Add labels and title
plt.title('Missing Data Over Time for Top Countries', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Number of Missing Values', fontsize=14)
plt.legend(title='Country')
plt.tight_layout()
plt.show()

# Fill using city-year averages
df['AverageTemperature'] = df.groupby(['City', 'year'])['AverageTemperature'].transform(
    lambda x: x.fillna(x.mean())
)

# Fill remaining NAs using country-year averages
df['AverageTemperature'] = df.groupby(['Country', 'year'])['AverageTemperature'].transform(
    lambda x: x.fillna(x.mean())
)

# Group by year and count missing values
missing_count = df.groupby('year')['AverageTemperature'].apply(lambda x: x.isna().sum())

# Convert to a DataFrame and rename columns for clarity
missing_count_df = missing_count.reset_index(name='missing_value')

# Plotting the missing data distribution with correct axis labels
plt.figure(figsize=(12, 6))
sns.histplot(data=missing_count_df, x='year', weights='missing_value', bins=70, kde=False)

# Add labels and titles
plt.title('Distribution of Missing Data by Year', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Number of Missing Values')
plt.tight_layout()
plt.show()

#Basic visualizations
plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
#Average temperature distribution
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

print("\nTop 10 Coldest Cities (Average):")
print(df.groupby('City')['AverageTemperature'].mean().sort_values().head(10))

# Temperature range by city
df_range = df.groupby('City').agg({
    'AverageTemperature': ['min', 'max']
}).reset_index()
df_range['temp_range'] = df_range['AverageTemperature']['max'] - df_range['AverageTemperature']['min']
df_range = df_range.sort_values('temp_range', ascending=False)

print("\nCities with Largest Temperature Ranges:")
print(df_range.head(10))



#MAP VISUALIZATION
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
df = pd.read_csv("C:/Users/Erdem/Desktop/UNIMI/codingfordse/Python/dataset_weather_majorcities.csv")

world = gpd.read_file(url)

# Filter data for 2010
df_2010 = df[df['year'] == 2010]

#average temperature for each city in 2010
city_temps = df_2010.groupby(['Country', 'City'])['AverageTemperature'].mean().reset_index()

#country averages based on city temperatures
country_temps = city_temps.groupby('Country')['AverageTemperature'].agg(
    AverageTemperature=('mean'),
    CityCount=('count')
).reset_index()

#Mapping
fig = px.choropleth(
    country_temps,
    locations='Country',
    locationmode='country names',
    color='AverageTemperature',
    hover_name='Country',
    hover_data={
        'AverageTemperature': ':.2f',
        'CityCount': True  # Show number of cities in hover tooltip
    },
    color_continuous_scale='RdBu_r',
    title='Average Temperatures by Country (2010) - Based on City Data',
    labels={
        'AverageTemperature': 'Temperature (°C)',
        'CityCount': 'Number of Cities'
    }
)
fig.update_layout(
    title_x=0.5,
    geo=dict(showframe=False, showcoastlines=True),
    width=1200,
    height=800
)
fig.show()

