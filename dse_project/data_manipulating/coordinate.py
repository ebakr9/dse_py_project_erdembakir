import pandas as pd
#Convert coordinates to values
def convert_coordinates(coord_str):
    if pd.isna(coord_str):
        return None
    
    coord_str = str(coord_str).strip()
    direction = coord_str[-1].upper()
    value = float(coord_str[:-1])
    
    if direction in ['S', 'W']:
        value = -value
    
    return value

def process_coordinates(df):
    df['Latitude'] = df['Latitude'].apply(convert_coordinates)
    df['Longitude'] = df['Longitude'].apply(convert_coordinates)
    return df