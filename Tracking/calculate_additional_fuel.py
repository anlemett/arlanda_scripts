import pandas as pd 
import os


def getAddFuel(fuel, CDO_fuel):

    return float(fuel)-float(CDO_fuel)


filename = os.path.join('data', 'fuel_consumption_2018_02.csv')
fuel_df = pd.read_csv(filename, sep=' ',
                    dtype={'fuel':float, 'CDO_fuel':float}
                    )

fuel_df['add_fuel'] = fuel_df.apply(lambda row: getAddFuel(row['fuel'], row['CDO_fuel']), axis=1)

fuel_df.to_csv(filename, sep=' ', encoding='utf-8', float_format='%.6f', index=False, header=True)
