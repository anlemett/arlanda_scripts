import pandas as pd


snow_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_snow_2018.csv", sep=' ')
cape_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cape_2018.csv", sep=' ')
wind_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_wind_2018.csv", sep=' ')


features_to_normalize = ['sd', 'rsn', 'sf']

snow_df[features_to_normalize] = snow_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

snow_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_snow_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')


features_to_normalize = ['cape']

cape_df[features_to_normalize] = cape_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

cape_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_cape_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')


features_to_normalize = ['i10fg', 'wind']

wind_df[features_to_normalize] = wind_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

wind_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_wind_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')