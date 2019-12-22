import pandas as pd

filename = "vfe_opensky_by_day_201801.csv"
df1 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201802.csv"
df2 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201803.csv"
df3 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201804.csv"
df4 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201805.csv"
df5 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201806.csv"
df6 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201807.csv"
df7 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201808.csv"
df8 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201809.csv"
df9 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201810.csv"
df10 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201811.csv"
df11 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})
filename = "vfe_opensky_by_day_201812.csv"
df12 = pd.read_csv(filename, sep=' ', names=['date', 'number_of_flights', 'total_number_of_levels', 'average_number_of_levels',
    'total_time_on_levels', 'average_time_on_levels', 'total_distance_on_levels', 'average_distance_on_levels'], dtype = {'date': str})

frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]

vfe_df = pd.concat(frames)

vfe_df.reset_index(drop=True, inplace=True)

filename = "vfe_opensky_by_day_2018.csv"
vfe_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.6f', header=None)
