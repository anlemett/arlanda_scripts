import pandas as pd

metar_df = pd.read_csv("metar_2018.csv", sep=' ', names=['date', 'time', 'metar'], dtype=str)
print(metar_df['date'])


def calculate_snow(metar_df):

    snow_df = pd.DataFrame(columns=['date', 'snow'])

    metar_df.set_index(['date'], inplace=True)

    for date, new_df in metar_df.groupby(level='date'):
        
        if new_df['metar'].str.contains("SN").empty:
            count = 0
        else:
            count = len(new_df[new_df['metar'].str.contains("SN").dropna()])
            #count = len(new_df[(new_df['metar'].str.contains("SN").dropna()) & (new_df['time'] >= '1150') & (new_df['time'] <= '1350')])
        print(count)

        #create df with date and snow count
        snow_df =snow_df.append({'date': date, 'snow': count}, ignore_index=True)

    #snow_df.to_csv("snow_by_day_2018.csv", sep=' ', encoding='utf-8', header=None)
    snow_df.to_csv("snow_by_day_2hours_2018.csv", sep=' ', encoding='utf-8', header=None)
    return snow_df

snow_df = calculate_snow(metar_df)
