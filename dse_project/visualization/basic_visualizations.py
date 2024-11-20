import matplotlib.pyplot as plt
import seaborn as sns

def plot_basic_distributions(df):
    plt.figure(figsize=(15, 6))
    
    # temp distribution
    plt.subplot(1, 2, 1)
    sns.histplot(data=df, x='AverageTemperature', bins=50)
    plt.title('Distribution of Average Temperatures')
    plt.xlabel('Temperature')

    # temp by year
    plt.subplot(1, 2, 2)
    df_yearly = df.groupby('year')['AverageTemperature'].mean().reset_index()
    sns.lineplot(data=df_yearly, x='year', y='AverageTemperature')
    plt.title('Average Temperature Over Years')
    plt.xlabel('Year')
    plt.ylabel('Average Temperature')
    plt.tight_layout()
    plt.show()
    return plt.gcf()

def plot_missing_data_distribution(df):
    missing_count = df.groupby('year')['AverageTemperature'].apply(lambda x: x.isna().sum())
    missing_count_df = missing_count.reset_index(name='missing_value')

    plt.figure(figsize=(12, 6))
    sns.histplot(data=missing_count_df, x='year', weights='missing_value', bins=70, kde=False)
    plt.title('Distribution of Missing Data by Year', fontsize=16)
    plt.xlabel('Year')
    plt.ylabel('Number of Missing Values')
    plt.tight_layout()
    plt.show()

    return plt.gcf()

def analyze_missing_data_by_country(df):
    # Calculate missing data by country and year
    missing_by_country = df.groupby(['Country', 'year'])['AverageTemperature'].apply(
        lambda x: x.isna().sum()
    ).reset_index(name='missing_count')
    
    # total missing data by country
    missing_country_summary = missing_by_country.groupby('Country')['missing_count'].sum().reset_index()
    missing_country_summary = missing_country_summary.sort_values(by='missing_count', ascending=False)
    
    #Plot total missing data by country
    plt.figure(figsize=(12, 6))
    sns.barplot(x='missing_count', y='Country', data=missing_country_summary.head(20))
    plt.title('Top 20 Countries with the Most Missing Data', fontsize=16)
    plt.xlabel('Total Missing Values')
    plt.ylabel('Country')
    plt.tight_layout()
    plt.show()

    #plot missing data over time for top countries
    top_countries = missing_country_summary.head(5)['Country']
    missing_top_countries = missing_by_country[missing_by_country['Country'].isin(top_countries)]
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=missing_top_countries, x='year', y='missing_count', hue='Country')
    plt.title('Missing Data Over Time for Top Countries', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Missing Values', fontsize=14)
    plt.legend(title='Country')
    plt.tight_layout()
    plt.show()
    return missing_country_summary.head(10), plt.gcf()

def plot_temperature_extremes(df):

    plt.figure(figsize=(10, 6))
    
    # Top 10 hottest cities
    top_10_hottest = df.groupby('City')['AverageTemperature'].mean().sort_values(
        ascending=False
    ).head(10).reset_index()
    
    # Add country information to city names
    top_10_hottest['City'] = top_10_hottest['City'].apply(
        lambda x: f"{x} ({df.loc[df['City'] == x, 'Country'].iloc[0]})"
    )
    
    sns.barplot(data=top_10_hottest, x='City', y='AverageTemperature')
    plt.title('Top 10 Hottest Cities (Average)')
    plt.xlabel('City (Country)')
    plt.ylabel('Average Temperature')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    # Get top 10 coldest cities
    top_10_coldest = df.groupby('City')['AverageTemperature'].mean().sort_values().head(10)
    plt.show()
    return plt.gcf(), top_10_coldest