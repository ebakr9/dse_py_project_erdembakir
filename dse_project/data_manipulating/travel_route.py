import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def find_closest_cities(current_city, cities_df):
    current_lat = cities_df.loc[cities_df['City'] == current_city, 'Latitude'].values[0]
    current_lon = cities_df.loc[cities_df['City'] == current_city, 'Longitude'].values[0]
    
    cities_df['Distance'] = cities_df.apply(lambda row: haversine(current_lat, current_lon, row['Latitude'], row['Longitude']), axis=1)
    closest_cities = cities_df.nsmallest(4, 'Distance')
    return closest_cities

def select_warmest_city(closest_cities):
    closest_cities = closest_cities[closest_cities['City'] != closest_cities.iloc[0]['City']] #not to select current city
    warmest_city = closest_cities.loc[closest_cities['AverageTemperature'].idxmax()]
    return warmest_city

def suggest_route(start_city, end_city, cities_df):
    current_city = start_city
    route = [current_city]
    
    while current_city != end_city:
        closest_cities = find_closest_cities(current_city, cities_df)
        warmest_city = select_warmest_city(closest_cities)
        
        route.append(warmest_city['City'])
        current_city = warmest_city['City']
    
    return route