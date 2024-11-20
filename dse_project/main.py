from data_manipulating.data_processing import load_and_prepare_data, filter_by_year, calculate_city_temperatures
from data_manipulating.coordinate import process_coordinates
from visualization.visualization import create_city_temperature_map
from config import SETTINGS, DATASETS
from visualization.basic_visualizations import plot_basic_distributions,plot_missing_data_distribution,plot_temperature_extremes,analyze_missing_data_by_country
def select_dataset():
    print("\nAvailable datasets:")
    for key, value in DATASETS.items():
        print(f"{key}: {value['description']}")
    
    while True:
        choice = input("\nSelect a dataset: ").strip().lower()
        if choice in DATASETS:
            return DATASETS[choice]['path']
        print("Invalid selection. Please try again.")

def main():
    # Let user select dataset
    selected_dataset = select_dataset()
    
    # Load and prepare data
    df = load_and_prepare_data(selected_dataset)
    
    # Process coordinates
    df = process_coordinates(df)
    #Descriptive statistics and plots
    basic_dist = plot_basic_distributions(df)
    missingdata = plot_missing_data_distribution(df)
    extreme_temp = plot_temperature_extremes(df)
    analyzemissingdata = analyze_missing_data_by_country(df)
    # Filter for target year
    df_filtered = filter_by_year(df, SETTINGS['target_year'])
    
    # Calculate city temperatures
    city_temps = calculate_city_temperatures(df_filtered)
    
    # Create and display map
    fig = create_city_temperature_map(
        city_temps, 
        width=SETTINGS['map_width'], 
        height=SETTINGS['map_height']
    )
    fig.show()

if __name__ == "__main__":
    main()