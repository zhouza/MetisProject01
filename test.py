from datetime import timedelta, date
import datetime
import numpy as np
import pandas as pd
import string
import re
import csv
import requests
import string

<<<<<<< HEAD
# initialize some variables
start_date = datetime.date.today()
end_date = datetime.date.today()
date_year = ''
date_month = ''
date_day = ''

=======
start_date = datetime.date(2018, 3, 31)
end_date = datetime.date(2018, 4, 7)

date_year = str(start_date.year)
date_month = str(start_date.month)
date_day = str(start_date.day)

data_url_date = date_year[2:] + date_month.zfill(2) + date_day.zfill(2)
>>>>>>> cb0b78109417230b983d0173997cd47a96d4e7e4
data_url_base = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
data_url_ext = '.txt'
data_url = data_url_base + data_url_date + data_url_ext

<<<<<<< HEAD
# define column names
cols_traffic = ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'EXITS']

# initialize an empty dataframe to store data inside
df_traffic = pd.DataFrame(columns = cols_traffic)

break_counter = 0

for year_counter in range(2015,2018):
    start_date = datetime.date(year_counter, 4, 14)
    end_date = datetime.date(year_counter, 6, 28)
    date_year = str(year_counter)
    # reset dataframe per year to empty
    df_traffic = pd.DataFrame(columns = cols_traffic)
    while (start_date <= end_date) and (break_counter < 10):
        # reset dataframe used in loop to empty
        df_loop = pd.DataFrame()
        # parse date into components
        date_month = str(start_date.month)
        date_day = str(start_date.day)
        # set YYMMDD format string for URL
        data_url_date = date_year[2:] + date_month.zfill(2) + date_day.zfill(2)
        # combined URL to use in request
        data_url = data_url_base + data_url_date + data_url_ext
        print(data_url)
        
        if requests.get(data_url).status_code == 404:
            # check next day until the right day of week is found
            start_date = start_date + datetime.timedelta(days = 1)
            break_counter += 1
        else:
            print('starting download')
            df_loop = pd.read_csv(data_url, delimiter = ',', names = cols_traffic, header = 0)
            # append dataframe from loop to the "master" dataframe
            df_traffic = pd.concat([df_traffic, df_loop])
            print('download completed')
            # increment by one week
            start_date = start_date + datetime.timedelta(days = 7)
        
        print('next date to pull: ', start_date)

    df_traffic.to_csv('traffic_' + date_year + '.txt', sep = ',', header = cols_traffic, index = False)

#print(df_traffic.columns)




"""
strip columns

turnstiles_df.DATE.value_counts().sort_index()
    # counts number of times that the date appears
    # index will sort by DATE because df.DATE returns a series where DATE is the index

"""
=======
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
>>>>>>> cb0b78109417230b983d0173997cd47a96d4e7e4
