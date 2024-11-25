import pandas as pd
import numpy as np
from .data_processing import filter_by_year
from .coordinate import process_coordinates,convert_coordinates

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def prepare_cities_data(df, year=None, aggregate_monthly=True):
    df = filter_by_year(df, year, aggregate_monthly=aggregate_monthly)
    
    cities_df = process_coordinates(df.copy())
    cities_df = cities_df.groupby([
        'City', 
        'Latitude', 
        'Longitude'
    ])['AverageTemperature'].mean().reset_index()
    
    # Remove NaN values
    cities_df = cities_df.dropna()
    
    return cities_df

def find_next_city(current_city, cities_df, visited_cities):
    current_data = cities_df.loc[cities_df['City'] == current_city]
    if current_data.empty:
        raise ValueError(f"City {current_city} not found in dataset!")
    
    current_lat = float(current_data['Latitude'].iloc[0])
    current_lon = float(current_data['Longitude'].iloc[0])
    
    #Calculate distances to all other cities
    distances = []
    for _, row in cities_df.iterrows():
        if row['City'] not in visited_cities:
            distance = haversine(
                current_lat, current_lon,
                float(row['Latitude']), float(row['Longitude'])
            )
            distances.append({
                'City': row['City'],
                'Distance': distance,
                'AverageTemperature': row['AverageTemperature']
            })
    # Convert to DataFrame and find hottest among nearest 3
    distances_df = pd.DataFrame(distances)
    nearest_3 = distances_df.nsmallest(3, 'Distance')
    hottest_city = nearest_3.loc[nearest_3['AverageTemperature'].idxmax()]
    
    return hottest_city['City']

def suggest_route(start_city, end_city, df, year=None, aggregate_monthly=True):
    cities_df = prepare_cities_data(df, year, aggregate_monthly)

    if start_city not in cities_df['City'].values:
        raise ValueError(f"Start city '{start_city}' not found in dataset")
    if end_city not in cities_df['City'].values:
        raise ValueError(f"End city '{end_city}' not found in dataset")
    
    current_city = start_city
    route = [current_city]
    visited_cities = {current_city}
    
    while current_city != end_city:
            next_city = find_next_city(current_city, cities_df, visited_cities)
            route.append(next_city)
            visited_cities.add(next_city)
            current_city = next_city 


    
    return route, cities_df
