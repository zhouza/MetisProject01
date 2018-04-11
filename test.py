from datetime import timedelta, date
import datetime
import numpy as np
import pandas as pd
import string
import re
import csv
import requests
import string

start_date = datetime.date(2018, 3, 31)
end_date = datetime.date(2018, 4, 7)

date_year = str(start_date.year)
date_month = str(start_date.month)
date_day = str(start_date.day)

data_url_date = date_year[2:] + date_month.zfill(2) + date_day.zfill(2)
data_url_base = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
data_url_ext = '.txt'
data_url = data_url_base + data_url_date + data_url_ext

# initialize an empty dataframe to store data inside
df_traffic = pd.DataFrame()

# define column names
cols_traffic = ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'EXITS']

while start_date <= end_date:
    df_loop = pd.DataFrame()
    
    date_year = str(start_date.year)
    date_month = str(start_date.month)
    date_day = str(start_date.day)

    data_url_date = date_year[2:] + date_month.zfill(2) + date_day.zfill(2)

    data_url = data_url_base + data_url_date + data_url_ext
    # print(data_url)
    
    if requests.get(data_url).status_code == 200:
        df_loop = pd.read_table(data_url, delimiter = ',', names = cols_traffic, skiprows = 1, skipinitialspace = True, lineterminator='\n')
        df_traffic = pd.concat([df_traffic, df_loop])
    else: print('Failed')
    
    # print(df_loop)
    
    # print(df_traffic)
    
    start_date = start_date + datetime.timedelta(days = 7)
    
print(df_traffic.head(10))
