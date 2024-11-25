import pandas as pd

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['dt'] = pd.to_datetime(df['dt'])
    df['year'] = df['dt'].dt.year
    return df

def filter_by_year(df, year, aggregate_monthly=False):
    filtered_df = df[df['year'] == year]
    if aggregate_monthly:
        return filtered_df.groupby([
            'Country',
            'City',
            'Latitude',
            'Longitude',
            'year'
        ])['AverageTemperature'].mean().reset_index()
    
    return filtered_df

def calculate_city_temperatures(df_filtered):
    return df_filtered.groupby(
        ['Country', 'City', 'Latitude', 'Longitude']
    )['AverageTemperature'].mean().reset_index()

def calculate_country_temperatures(df_filtered):
    # Group by country and calculate mean temperature
    return df_filtered.groupby('Country')['AverageTemperature'].mean().reset_index()

def calculate_state_temperatures(df_filtered):
    return df_filtered.groupby(['State', 'Country'])['AverageTemperature'].mean().reset_index()