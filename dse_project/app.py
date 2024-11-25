import streamlit as st
import pandas as pd
from data_manipulating.data_processing import load_and_prepare_data, filter_by_year, calculate_city_temperatures, calculate_country_temperatures,calculate_state_temperatures
from data_manipulating.coordinate import process_coordinates
from visualization.visualization import create_city_temperature_map, create_country_temperature_map,create_state_temperature_map
from visualization.basic_visualizations import (
    plot_basic_distributions,
    plot_missing_data_distribution,
    plot_temperature_extremes,
    analyze_missing_data_by_country
)
from config import DATASETS, SETTINGS
import time
from data_manipulating.travel_route import suggest_route


if 'animation_running' not in st.session_state:
    st.session_state.animation_running = False
if 'current_year' not in st.session_state:
    st.session_state.current_year = SETTINGS['target_year']

st.set_page_config(
    page_title="Global Temperature Analysis",
    page_icon="🌡️",
    layout="wide"
)

st.title("Global Temperature Analysis")
st.markdown("Analyze historical temperature data across different geographical locations.")

#Dataset selection
selected_dataset = st.sidebar.selectbox(
    "Select Dataset",
    options=list(DATASETS.keys()),
    format_func=lambda x: DATASETS[x]['description']
)

#load data
@st.cache_data #it is for holding data in cache which makes faster app 
def load_data(dataset_key):
    df = load_and_prepare_data(DATASETS[dataset_key]['path'])
    if DATASETS[dataset_key]['needs_preprocess']:
        df = process_coordinates(df)
    return df

# Load the selected dataset
with st.spinner('Loading data...'):
    df = load_data(selected_dataset)
    st.success('Data loaded successfully!')

# Analysis options in sidebar
analysis_option = st.sidebar.selectbox(
    "Choose Analysis",
    ["Basic Statistics", "Temperature Distribution", "Missing Data Analysis", "Temperature Extremes","Temperature Map","Travel Route"]
)

# Main content area
if analysis_option == "Basic Statistics":
    st.header("Basic Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Summary")
        st.write(df.describe())
    
    with col2:
        st.subheader("Dataset Info")
        st.write(f"Total Records: {len(df)}")
        st.write(f"Date Range: {df['year'].min()} - {df['year'].max()}")
        st.write(f"Number of Cities: {df['City'].nunique()}" if 'City' in df.columns else "")

elif analysis_option == "Temperature Distribution":
    st.header("Temperature Distribution")
    fig = plot_basic_distributions(df)
    st.pyplot(fig)

elif analysis_option == "Missing Data Analysis":
    st.header("Missing Data Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = plot_missing_data_distribution(df)
        st.pyplot(fig1)
    
    with col2:
        missing_summary, fig2 = analyze_missing_data_by_country(df)
        st.pyplot(fig2)


elif analysis_option == "Temperature Extremes":
    st.header("Temperature Extremes")
    fig, _ = plot_temperature_extremes(df)
    st.pyplot(fig)

elif analysis_option == "Temperature Map":
    st.header("Temperature Map")
    
    
    if DATASETS[selected_dataset]['type'] == 'city':
        def update_map(year_val, container):
            df_filtered = filter_by_year(df, year_val)
            city_temps = calculate_city_temperatures(df_filtered)
            fig = create_city_temperature_map(city_temps)
            fig.update_layout(title=f'Average Temperatures by City ({year_val})')
            container.plotly_chart(fig, use_container_width=True)
            st.session_state.current_year = year_val
        
        col1, col2, col3 = st.columns([2, 0.5, 0.5])
        
        with col1:
            year = st.slider("Select Year", 
                           min_value=int(df['year'].min()),
                           max_value=int(df['year'].max()),
                           value=st.session_state.current_year,
                           key='year_slider')
        
        with col2:
            play = st.button("Play", key="play_button")
        
        with col3:
            stop = st.button("Stop", key="stop_button")
        
        # Container for the map
        map_container = st.empty()
        
        if play:
            st.session_state.animation_running = True
        if stop:
            st.session_state.animation_running = False
        
        if st.session_state.animation_running:
            # Animation loop startinsg from selected year
            for year_val in range(year, int(df['year'].max()) + 1):
                if not st.session_state.animation_running:
                    break
                update_map(year_val, map_container)
                time.sleep(0.5)
            # Reset animation state when it reaches the end
            st.session_state.animation_running = False
        else:
            # Update map based on current year
            update_map(st.session_state.current_year, map_container)
    
    elif DATASETS[selected_dataset]['type'] == 'state':
        def update_state_map(year_val, container):
            df_filtered = filter_by_year(df, year_val)
            state_temps = calculate_state_temperatures(df_filtered)
            fig = create_state_temperature_map(state_temps)
            fig.update_layout(title=f'Average Temperatures by State ({year_val})')
            container.plotly_chart(fig, use_container_width=True)
            st.session_state.current_year = year_val
        
        col1, col2, col3 = st.columns([2, 0.5, 0.5])
        
        with col1:
            year = st.slider("Select Year", 
                           min_value=int(df['year'].min()),
                           max_value=int(df['year'].max()),
                           value=st.session_state.current_year,
                           key='year_slider')
        
        with col2:
            play = st.button("Play", key="play_button")
        
        with col3:
            stop = st.button("Stop", key="stop_button")
        
        # Container for the map
        map_container = st.empty()
        
        if play:
            st.session_state.animation_running = True
        if stop:
            st.session_state.animation_running = False
        
        if st.session_state.animation_running:
            for year_val in range(year, int(df['year'].max()) + 1):
                if not st.session_state.animation_running:
                    break
                update_state_map(year_val, map_container)
                time.sleep(0.5)
            st.session_state.animation_running = False
        else:
            update_state_map(year, map_container)
    
    else:  # country type
        def update_country_map(year_val, container):
            df_filtered = filter_by_year(df, year_val)
            country_temps = calculate_country_temperatures(df_filtered)
            fig = create_country_temperature_map(country_temps)
            fig.update_layout(title=f'Average Temperatures by Country ({year_val})')
            container.plotly_chart(fig, use_container_width=True)
            st.session_state.current_year = year_val
        
        col1, col2, col3 = st.columns([2, 0.5, 0.5])
        
        with col1:
            year = st.slider("Select Year", 
                           min_value=int(df['year'].min()),
                           max_value=int(df['year'].max()),
                           value=st.session_state.current_year,
                           key='year_slider')
        
        with col2:
            play = st.button("Play", key="play_button")
        
        with col3:
            stop = st.button("Stop", key="stop_button")
        
        # Container map
        map_container = st.empty()
        
        if play:
            st.session_state.animation_running = True
        if stop:
            st.session_state.animation_running = False
        
        if st.session_state.animation_running:
            for year_val in range(year, int(df['year'].max()) + 1):
                if not st.session_state.animation_running:
                    break
                update_country_map(year_val, map_container)
                time.sleep(0.5)
            st.session_state.animation_running = False
        else:
            update_country_map(year, map_container)
elif analysis_option == "Travel Route":
    st.header("Temperature-Based Travel Route")
    st.markdown("Find a route between two cities that passes through the hottest nearby cities.")
    
    if DATASETS[selected_dataset]['type'] != 'city':
        st.warning("This analysis is only available for city-level datasets.")
    else:
        # Get list of cities and years
        available_cities = sorted(df['City'].unique())
        available_years = sorted(df['year'].unique())
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            start_city = st.selectbox(
                "Select Start City", 
                available_cities, 
                key='start_city'
            )
        with col2:
            end_city = st.selectbox(
                "Select End City", 
                available_cities, 
                key='end_city'
            )
        with col3:
            selected_year = st.selectbox(
                "Select Year", 
                available_years,
                key='route_year'
            )
        
        if st.button("Find Route"):
            if start_city == end_city:
                st.warning("Please select different start and end cities.")
            else:
                    # Find route
                    route, cities_df = suggest_route(
                        start_city, 
                        end_city, 
                        df,
                        year=selected_year,
                        aggregate_monthly=True  # Always True for yearly averages
                    )
                    
                    # Display route
                    st.subheader("Suggested Route:")
                    route_str = " → ".join(route)
                    st.write(route_str)
                    
                    # a map showing the route
                    route_df = cities_df[cities_df['City'].isin(route)].copy()
                    route_df['order'] = route_df['City'].map({city: i for i, city in enumerate(route)})
                    route_df = route_df.sort_values('order')
                    
                    # Map title with year
                    map_title = f"Route Map ({selected_year})"
                    
                    import plotly.express as px
                    fig = px.line_mapbox(route_df, 
                                       lat='Latitude', 
                                       lon='Longitude',
                                       hover_name='City',
                                       hover_data=['AverageTemperature'],
                                       title=map_title)
                    
                    fig.add_scattermapbox(lat=route_df['Latitude'],
                                        lon=route_df['Longitude'],
                                        mode='markers+text',
                                        text=route_df['City'],
                                        textposition='top center',
                                        showlegend=False)
                    
                    fig.update_layout(mapbox_style='carto-positron',
                                    mapbox=dict(zoom=2),
                                    margin={"r":0,"t":30,"l":0,"b":0})
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display temperature information
                    st.subheader("Temperature Details:")
                    temp_df = route_df[['City', 'AverageTemperature']].copy()
                    temp_df['AverageTemperature'] = temp_df['AverageTemperature'].round(2)
                    temp_df.columns = ['City', 'Average Temperature (C)']
                    st.dataframe(temp_df)
