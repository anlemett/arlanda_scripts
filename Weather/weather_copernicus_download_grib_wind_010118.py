import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', 'instantaneous_10m_wind_gust',
        ],
	'area': '61/17/59/19',
        'year': '2018',
        'month': [
            '01',
        ],
        'day': [
            '01'
        ],
        'time': [
            '00:00', '01:00', '02:00',
            '03:00', '04:00', '05:00',
            '06:00', '07:00', '08:00',
            '09:00', '10:00', '11:00',
            '12:00', '13:00', '14:00',
            '15:00', '16:00', '17:00',
            '18:00', '19:00', '20:00',
            '21:00', '22:00', '23:00',
        ],
        'format': 'grib',
    },
    'data/weather_copernicus_TMA_grib_2018/copernicus_TMA_wind_010118.grib')