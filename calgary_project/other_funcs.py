import pandas as pd
def get_seasons(data: pd.DataFrame):
    data['season'] = data['month'] % 12 // 3 + 1
    season_dict = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    data['season'] = data['season'].map(season_dict)

    return data