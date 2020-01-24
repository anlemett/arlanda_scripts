import pandas as pd


metar_df = pd.read_csv("data/weather_metar_csv_2018/metar_snow_by_day_2018.csv", sep=' ',
                      names=['date', 'snow'], dtype = {'date': str})


features_to_normalize = ['snow']

metar_df[features_to_normalize] = metar_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

metar_df.to_csv("data/weather_metar_csv_2018/metar_snow_by_day_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')
