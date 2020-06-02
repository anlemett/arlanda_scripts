import pandas as pd
import os

year = '2018'

DATA_INPUT_DIR = os.path.join("data", "states_TMA_opensky_merged_with_ddr_m3_" + year)

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for month in months:
    print(month)
    
    filename = "states_TMA_opensky_" + year + "_"+ month + ".csv"
    full_filename = os.path.join(DATA_INPUT_DIR, filename)

    df = pd.read_csv(full_filename, sep=' ',
                     names = ['flightId', 'sequence', 'timestamp', 'lat', 'lon', 'altitude', 'velocity', 'endDate', 'aircraftType'],
                     dtype=str)
    

    df = df[df.timestamp != "time"]


    df.to_csv(full_filename, sep=' ', encoding='utf-8', float_format='%.3f', header=False, index=False)
