import pandas as pd


noaa_df = pd.read_csv("data/weather_noaa_TMA_csv_2018/noaa_2018.csv", sep=' ',
                      names=['date', 'lat', 'lon', 'visibility', 'cape', 'gust'], dtype = {'date': str})


features_to_normalize = ['visibility', 'cape', 'gust']

noaa_df[features_to_normalize] = noaa_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

noaa_df.to_csv("data/weather_noaa_TMA_csv_2018/noaa_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')
