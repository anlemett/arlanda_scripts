import pandas as pd


add_weather_df = pd.read_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_add_weather_2018.csv", sep=' ')

# 't2m', 'crr', 'csf', 'csfr', 'hcc', 'lcc', 'mcpr', 'msr', 'mtpr', 'mcc'

# t2m min - 254.653, t2m max - 306.329
# crr min - 0.0, crr max - 0.006
# csf min - 0.0, csf max - 0.001
# csfr min - 0.0, csfr max - 0.002
# hcc min - 0.0, hcc max - 1.0
# lcc min - 0.0, lcc max - 1.0
# mcpr min - 0.0, mcpr max - 0.003
# msr min - 0.0, mcr max - 0.001
# mtpr min - 0.0, mtpr max - 0.003
# mcc min - 0.0, mcc max - 1.0


features_to_normalize = ['t2m']

add_weather_df[features_to_normalize] = add_weather_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

add_weather_df = add_weather_df[['month', 'day', 'hour', 't2m', 'crr', 'csf', 'csfr', 'hcc', 'lcc', 'mcpr', 'msr', 'mtpr', 'mcc']]

add_weather_df.to_csv("data/weather_copernicus_TMA_csv_2018/copernicus_TMA_add_weather_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')

