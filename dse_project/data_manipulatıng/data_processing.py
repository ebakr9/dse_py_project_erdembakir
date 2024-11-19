import pandas as pd

def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df['dt'] = pd.to_datetime(df['dt'])
    df['year'] = df['dt'].dt.year
    return df

def filter_by_year(df, year):
    return df[df['year'] == year]

def calculate_city_temperatures(df_filtered):
    return df_filtered.groupby(
        ['Country', 'City', 'Latitude_num', 'Longitude_num']
    )['AverageTemperature'].mean().reset_index()