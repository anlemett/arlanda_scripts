import pandas as pd

month = "2018_01"

METAR_TXT = "ESSA_metar_" + month + ".txt"
METAR_CSV = "metar_" + month + ".csv"

def getDate(datetime_str):
    # old format: yyyy-mm-dd
    # new format: yymmdd

    return str(datetime_str[2:4] + datetime_str[5:7] + datetime_str[8:10])

def getTime(datetime_str):
    # old format: hh:mm
    # new format: hhmm

    return str(datetime_str[11:13] + datetime_str[14:])



df = pd.read_csv(METAR_TXT, sep=',', dtype=str)

metar_df = pd.DataFrame(columns=['date', 'time', 'metar'], dtype=str)

metar_df['date'] = df.apply(lambda row: getDate(row['valid']), axis=1)
metar_df['time'] = df.apply(lambda row: getTime(row['valid']), axis=1)
metar_df['metar'] = df['metar']

metar_df.to_csv(METAR_CSV, sep=',', encoding='utf-8', header=None, index=False)
