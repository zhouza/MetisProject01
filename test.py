import numpy as np
import pandas as pd
import string
import re
import csv

from datetime import timedelta, date
import requests
import string

start_date = datetime.date(2015, 1, 1)
end_date = datetime.date(2015, 1, 10)

#date.today()
"""
data_url_base = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
data_url_date = ''
data_url = data_url_base + data_url_date
data_url_ext = '.txt'

# initialize an empty dataframe to store data inside
df_transaction = pd.DataFrame()

while start_date <= end_date:
    df_loop = pd.DataFrame()
    
    date_year = str(start_date.year)
    date_month = str(start_date.month)
    date_day = str(start_date.day)

    data_url_date = date_year[2:] + date_month.zfill(2) + date_day.zfill(2)

    data_url = data_url_base + data_url_date + data_url_ext
    # print(data_url)
    
    if request.status_code == 200:
        df_loop = pd.read_csv(data_url, delimiter = ',', inplace = True)
        df_transaction = pd.concat([df_transaction, df_loop])
    
    # print(df_loop)
    
    # print(df_transaction)
    
    start_date = start_date + datetime.timedelta(days = 1)
    
print(df_transaction.head(10))

"""

data_url_base = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_'
data_url_date = ''
data_url = data_url_base + data_url_date
data_url_ext = '.txt'

# initialize an empty dataframe to store data inside
df_transaction = pd.DataFrame()

df_loop = pd.DataFrame()

start_date = datetime.date(2015, 1, 3)
end_date = datetime.date(2015, 1, 10)
date_year = str(start_date.year)
date_month = str(start_date.month)
date_day = str(start_date.day)
data_url_date = date_year[2:] + date_month.zfill(2) + date_day.zfill(2)
data_url = data_url_base + data_url_date + data_url_ext

df_loop = pd.read_csv(data_url, delimiter = ',')
df_transaction.append(df_loop)


# In[96]:


df_transaction = pd.concat([df_transaction, df_loop])


# In[102]:


df_transaction.isnull().sum()


# In[106]:


df_transaction['TOT_MOVEMENT'] = df.apply(lambda row: row['ENTRIES'] + row['EXITS'], axis=1)


# In[ ]:


df_transaction.loc[df_transaction.=='Male',]

