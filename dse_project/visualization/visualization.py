import plotly.express as px

def create_city_temperature_map(city_temps, width=1200, height=800):
    fig = px.scatter_geo(
        city_temps,
        lat='Latitude_num',
        lon='Longitude_num',
        color='AverageTemperature',
        hover_name='City',
        hover_data={
            'Country': True,
            'AverageTemperature': ':.2f',
            'Latitude_num': ':.2f',
            'Longitude_num': ':.2f'
        },

        color_continuous_scale='RdBu_r', 
        title='Average Temperatures by City (2010)',
        labels={
            'AverageTemperature': 'Temperature (°C)',
            'Latitude_num': 'Latitude',
            'Longitude_num': 'Longitude'
        }
    )

    fig.update_traces(
        marker=dict(
            size=8,
            opacity=0.8,
            line=dict(width=1, color='black') 
        )
    )

    fig.update_layout(
        title_x=0.5,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular',
            landcolor='lightgray',  
            oceancolor='aliceblue',  
            showocean=True,
            coastlinecolor='white', 
            countrycolor='white'   
        ),
        width=width,
        height=height
    )
    
    return fig