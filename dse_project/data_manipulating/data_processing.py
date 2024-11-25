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

def analyze_temperature_ranges(df, start_year=None, end_year=None):
    """
    Analyze temperature ranges for cities within specified time period.
    
    Args:
        df: DataFrame with temperature data
        start_year: Start year for analysis (optional)
        end_year: End year for analysis (optional)
    
    Returns:
        DataFrame with city temperature range statistics
    """
    # Filter by year range if specified
    if start_year and end_year:
        df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    
    # Calculate temperature ranges and statistics for each city
    temp_ranges = df.groupby(['City', 'Latitude_num', 'Longitude_num']).agg({
        'AverageTemperature': [
            'min',
            'max',
            'mean',
            'std'
        ]
    }).reset_index()
    
    # Flatten column names
    temp_ranges.columns = ['City', 'Latitude', 'Longitude', 
                          'Min_Temp', 'Max_Temp', 'Mean_Temp', 'Std_Temp']
    
    # Calculate temperature range
    temp_ranges['Temp_Range'] = temp_ranges['Max_Temp'] - temp_ranges['Min_Temp']
    
    # Sort by temperature range in descending order
    temp_ranges = temp_ranges.sort_values('Temp_Range', ascending=False)
    
    return temp_ranges