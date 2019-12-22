import pandas as pd

csv_input_file = "statistics_ddr_by_day_2018.csv"
ddr_stat_df = pd.read_csv(csv_input_file, sep=' ',
                     names = ['endDate', 'number_of_flights', 'delayed_5_min_flights_number', 'delayed_15_min_flights_number',
                              'total_departure_delay', 'average_departure_delay', 'total_arrival_delay', 'average_arrival_delay',
                              'average_add_time'],
                     index_col=[0],
                     dtype={'flightId':int, 'endDate':str, 'endTime':str, 'departure_delay':int, 'arrival_delay':int, 'add_time':int})


av_percent_delayed_df = pd.DataFrame(columns = ['month', 'av_percent_delayed'])

df = ddr_stat_df[(ddr_stat_df['endDate']>='180101')&(ddr_stat_df['endDate']<='180131')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':1, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180201')&(ddr_stat_df['endDate']<='180228')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':2, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180301')&(ddr_stat_df['endDate']<='180331')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':3, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180401')&(ddr_stat_df['endDate']<='180430')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':4, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180501')&(ddr_stat_df['endDate']<='180531')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':5, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180601')&(ddr_stat_df['endDate']<='180630')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':6, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180701')&(ddr_stat_df['endDate']<='180731')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':7, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180801')&(ddr_stat_df['endDate']<='180831')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':8, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='180901')&(ddr_stat_df['endDate']<='180930')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':9, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='181001')&(ddr_stat_df['endDate']<='181031')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':10, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='181101')&(ddr_stat_df['endDate']<='181130')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':11, 'av_percent_delayed':av}, ignore_index=True)

df = ddr_stat_df[(ddr_stat_df['endDate']>='181201')&(ddr_stat_df['endDate']<='181231')]
av = df["delayed_15_min_flights_number"].sum()/df["number_of_flights"].sum()*100
av_percent_delayed_df = av_percent_delayed_df.append({'month':12, 'av_percent_delayed':av}, ignore_index=True)

av_percent_delayed_df.to_csv("percent_of_delayed_by_month.csv", sep=' ', encoding='utf-8', float_format='%.3f', header=None, index=False)

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.xlabel('Months', fontsize=25)
plt.ylabel('Delayed flights [%]', fontsize=25)
    
plt.tick_params(labelsize=20)
x = [1,2,3,4, 5, 6, 7, 8, 9, 10, 11, 12]
plt.xticks(np.arange(min(x), max(x)+1, 1.0))

plt.plot(x, av_percent_delayed_df['av_percent_delayed'], color="darkorange", linewidth=5)

plt.savefig("delayed_flights_by_month.png")
    
    
    
    
    