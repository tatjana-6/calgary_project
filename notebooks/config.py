# Default values for plotting functions 
eda_ridership_defaults = {
    'plot_seasonal_and_total_trends': {
        'y': 'ridership',
        'dataset': 'Ridership',
        'fig_dime': (10, 6)

    }
}


eda_tpo_calls_defaults = {
    'plot_yearly_sum_trend': {
        'y': 'activity_number',
        'dataset': 'TPO',
    },
    'plot_seasonal_and_total_trends': {
        'y': 'activity_number',
        'dataset': 'TPO',
    }
}
