import pandas as pd

filename = "metar_2018_01.csv"
df1 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_02.csv"
df2 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_03.csv"
df3 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_04.csv"
df4 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_05.csv"
df5 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_06.csv"
df6 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_07.csv"
df7 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_08.csv"
df8 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_09.csv"
df9 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_10.csv"
df10 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_11.csv"
df11 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)
filename = "metar_2018_12.csv"
df12 = pd.read_csv(filename,  sep=',', names=['date', 'time', 'metar'], dtype=str)


frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]

metar_df = pd.concat(frames)
metar_df.reset_index(drop=True, inplace=True)

filename = "metar_2018.csv"
metar_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.6f', header=None)
