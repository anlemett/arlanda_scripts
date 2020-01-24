import pandas as pd


ddr_stat_df = pd.read_csv("data/statistics_ddr_2018/statistics_ddr_by_hour_2018.csv", sep=' ', index_col=0)
opensky_stat_df = pd.read_csv("data/statistics_opensky_2018/statistics_opensky_by_hour_2018.csv", sep=' ', index_col=0)


features_to_normalize = ['number_of_flights']

ddr_stat_df[features_to_normalize] = ddr_stat_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

ddr_stat_df.to_csv("data/statistics_ddr_2018/statistics_ddr_by_hour_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')


opensky_stat_df[features_to_normalize] = opensky_stat_df[features_to_normalize].apply(lambda x:(x-x.min()) / (x.max()-x.min()))

opensky_stat_df.to_csv("data/statistics_opensky_2018/statistics_opensky_by_hour_norm_2018.csv", sep=' ', float_format='%.6f', encoding='utf-8')