def analyze_temperature_ranges(df, start_year=None, end_year=None):
    if start_year and end_year:
        df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    
    #Calculate temperature ranges
    temp_ranges = df.groupby(['City', 'Latitude', 'Longitude']).agg({
        'AverageTemperature': [
            'min',
            'max',
            'mean',
            'std'
        ]
    }).reset_index()
    
    temp_ranges.columns = ['City', 'Latitude', 'Longitude', 
                          'Min_Temp', 'Max_Temp', 'Mean_Temp', 'Std_Temp']

    temp_ranges['Temp_Range'] = temp_ranges['Max_Temp'] - temp_ranges['Min_Temp']

    temp_ranges = temp_ranges.sort_values('Temp_Range', ascending=False)
    
    return temp_ranges