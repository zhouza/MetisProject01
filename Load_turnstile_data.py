from dateutil.relativedelta import relativedelta
from datetime import timedelta, date
import datetime
import numpy as np
import pandas as pd
import string
import re
import csv
import requests
import string

def load_turnstile_data(startdate_str,enddate_str,years_hist):
    """
    This function will load turnstile data into a singular csv output file based on 
    whether the datestamp for each dataset falls within the input range. Each dataset 
    contains a week's worth of data so it is recommended that the input range be widened
    to select more data. 
    Inputs: 
        startdate_str as a string in 'YYYYMMDD' format
        enddate_str as a string in 'YYYYMMDD' format
        years_hist as int, representing how many years of history to load
    Dates must be in the past.
    """
    # ensure input types are correct
    try:
        datetime.date(int(startdate_str[0:4]),int(startdate_str[4:6]),int(startdate_str[6:]))
    except TypeError:
        print("start_date input must be a string of form 'YYYYMMDD'")
        raise
    try:
        datetime.date(int(enddate_str[0:4]),int(enddate_str[4:6]),int(enddate_str[6:]))
    except TypeError:
        print("end_date input must be a string of form 'YYYYMMDD'")
        raise
    try:
        int(years_hist)
    except TypeError:
        print("years_hist input must be an integer")
        raise
    
    today_check = datetime.date.today()
    
    # convert string inputs to date
    start_date = datetime.date(int(startdate_str[0:4]),int(startdate_str[4:6]),int(startdate_str[6:]))
    end_date = datetime.date(int(enddate_str[0:4]),int(enddate_str[4:6]),int(enddate_str[6:]))
    
    if (start_date > today_check) or (end_date > today_check):
        return('input range must be in the past')
    else:
        # initialize some variables
        date_month = ''
        date_day = ''
        date_year = start_date.year

        data_url_base = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
        data_url_ext = '.txt'

        # define column names because I couldn't figure out how to strip the spaces when this was written
        cols_traffic = ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME', 'DESC', 'ENTRIES', 'EXITS']

        # initialize an empty dataframe to store data inside
        df_traffic = pd.DataFrame(columns = cols_traffic)

        # set a break counter to prevent infinite looping
        break_counter = 0

        # lookback must be redefined since it is inclusive
        year_diff = years_hist
        # loop through each year in the year_hist range to pull the data relevant to the timeframe per year
        for year_counter in range(0,year_diff):
            loop_start_date = start_date + relativedelta(years=-(year_diff-year_counter-1))
            loop_end_date = end_date + relativedelta(years=-(year_diff-year_counter-1))
            break_counter = 0
            while (loop_start_date <= loop_end_date) and (break_counter < 10):
                # reset dataframe used in loop to empty
                df_loop = pd.DataFrame()
                # parse date into components
                date_month = str(loop_start_date.month)
                date_day = str(loop_start_date.day)
                date_year = str(loop_start_date.year)
                # set YYMMDD format string for URL
                data_url_date = date_year[2:] + date_month.zfill(2) + date_day.zfill(2)
                # combined URL to use in request
                data_url = data_url_base + data_url_date + data_url_ext
                print(data_url)

                if requests.get(data_url).status_code == 404:
                    # check next day until the right day of week is found
                    loop_start_date = loop_start_date + datetime.timedelta(days = 1)
                    break_counter += 1
                else:
                    print('starting download')
                    df_loop = pd.read_csv(data_url, delimiter = ',', names = cols_traffic, header = 0)
                    # append dataframe from loop to the "master" dataframe
                    df_traffic = pd.concat([df_traffic, df_loop])
                    print('download completed')
                    # increment by one week
                    loop_start_date = loop_start_date + datetime.timedelta(days = 7)

                print('next date to pull: ', loop_start_date)

        df_traffic.to_csv('traffic1.csv', sep = ',', header = cols_traffic, index = False)
    return()

load_turnstile_data('20170423','20170521',3)