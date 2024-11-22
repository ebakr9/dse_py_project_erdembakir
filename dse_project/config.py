# Configuration settings
DATASETS = {
    'major_cities_data': {
        'path': 'C:/Users/Erdem/Desktop/UNIMI/dse_project/data/GlobalLandTemperaturesByMajorCity.csv',
        'description': 'Temperature data for major cities worldwide',
        'needs_preprocess':True,
        'type':'city'
    },

    'country_data': {
        'path': 'C:/Users/Erdem/Desktop/UNIMI/dse_project/data/GlobalLandTemperaturesByCountry.csv',
        'description': 'Temperature data for countries in the world',
        'needs_preprocess':False,
        'type':'country'
    },

    'all_cities_data':{
        'path':'C:/Users/Erdem/Desktop/UNIMI/dse_project/data/GlobalLandTemperaturesByCity.csv',
        'description': 'Temperature data for more cities in the world.',
        'needs_preprocess':True,
        'type':'city'
    },

    'state_data':{
        'path':'C:/Users/Erdem/Desktop/UNIMI/dse_project/data/GlobalLandTemperaturesByState.csv',
        'description':' Temperature data for staten is the world',
        'needs_preprocess':False,
        'type':'state'
    }
}

SETTINGS = {
    'map_width': 1200,
    'map_height': 800,
    'target_year': 2010
}