import plotly.express as px

def create_city_temperature_map(city_temps, width=1200, height=800):
    fig = px.scatter_geo(
        city_temps,
        lat='Latitude',
        lon='Longitude',
        color='AverageTemperature',
        hover_name='City',
        hover_data={
            'Country': True,
            'AverageTemperature': ':.2f',
            'Latitude': ':.2f',
            'Longitude': ':.2f'
        },

        color_continuous_scale='RdBu_r', 
        title='Average Temperatures by City (2010)',
        labels={
            'AverageTemperature': 'Temperature (°C)',
            'Latitude': 'Latitude',
            'Longitude': 'Longitude'
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


def create_country_temperature_map(country_temps, width=1200, height=800):
    fig = px.choropleth(
        country_temps,
        locations='Country', 
        locationmode='country names',  
        color='AverageTemperature',
        hover_data={
            'Country': True,
            'AverageTemperature': ':.2f'
        },
        color_continuous_scale='RdBu_r',
        title='Average Temperatures by Country',
        labels={
            'AverageTemperature': 'Temperature (°C)',
            'Country': 'Country'
        }
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

def create_state_temperature_map(state_temps, width=1200, height=800):
    state_temps['location'] = state_temps['State'] + ', ' + state_temps['Country']
    
    fig = px.choropleth(
        state_temps,
        locations='location',
        locationmode='country names',
        color='AverageTemperature',
        hover_data={
            'State': True,
            'Country': True,
            'AverageTemperature': ':.2f'
        },
        color_continuous_scale='RdBu_r',
        title='Average Temperatures by State',
        labels={
            'AverageTemperature': 'Temperature (°C)',
            'State': 'State',
            'Country': 'Country'
        }
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