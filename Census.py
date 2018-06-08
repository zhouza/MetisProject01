from datetime import timedelta, date
import datetime
import numpy as np
import pandas as pd
import string
import re
import csv
import requests
import string
from copy import deepcopy, copy
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import scipy

get_ipython().run_line_magic('matplotlib', 'inline')

plt.style.use('seaborn')

def find_nearest(ref_array,target_array):
    """
    This function takes in a reference array and a target array, 
    and returns a list of indices corresponding to the reference array
    representing the nearest location for each element in the target array.
    """
    ref_tree = scipy.spatial.cKDTree(ref_array)
    dist, indices = ref_tree.query(target_array, k=1)
    return indices

# read data from saved csv files
df_census = pd.read_csv('nyc_census_tracts.csv', delimiter = ',', header = 0, skipinitialspace = True)
df_census_loc = pd.read_csv('census_block_loc.csv', delimiter = ',', header = 0, skipinitialspace = True)
df_stations = pd.read_csv('stations.csv', delimiter = ',', header = 0, skipinitialspace = True)

# create a new dataframe with only the columns we are interested in
df_census_sub = df_census[["CensusTract","County","Borough","TotalPop","Women","Income","Poverty","Professional","Transit","Employed"]].copy()
# select only census data from within NY
df_census_loc = df_census_loc[(df_census_loc["State"] == 'NY')]

# The census location data has an identifier for the census block, but this identifier has more digits to signify a more specific location slice. In order to match up the location with the census data, we need to cut down the identifier to the appropriate specificity. 
# create a copy of the BlockCode as a string so that we can perform slicing
df_census_loc["CensusTract"] = df_census_loc["BlockCode"].apply(str)
df_census_loc["CensusTract"] = df_census_loc["CensusTract"].str[:-4]

# set the CensusTract string back to an integer type so that the data types will match when merging later on
df_census_loc["CensusTract"] = df_census_loc["CensusTract"].apply(int)

# Find the average coordinates for each CensusTract
df_census_loc["Avg_Lat"] = df_census_loc.groupby(["CensusTract"])["Latitude"].transform(lambda x: x.mean())
df_census_loc["Avg_Long"] = df_census_loc.groupby(["CensusTract"])["Longitude"].transform(lambda x: x.mean())

# create a new dataframe that contains only CensusTract ID and the matching average geographical coordinates
df_census_coord = df_census_loc[["CensusTract","Avg_Lat","Avg_Long"]].copy()

# drop duplicates so there is only one record per CensusTract. the duplicates came from the transform function above.
df_census_coord.drop_duplicates(["CensusTract","Avg_Lat","Avg_Long"], keep = 'first', inplace = True)

# create a new dataframe by adding 3 columns from our location dataframe into the census data dataframe
df_census_merge = pd.merge(df_census_sub,df_census_coord[["CensusTract","Avg_Lat","Avg_Long"]],on='CensusTract')

df_census_sex = df_census_merge[["CensusTract","County","Borough","TotalPop","Women","Avg_Lat","Avg_Long"]].copy()

"""
# compare how many non-responses would be removed compared to the full dataset sizsei
df_census_sex[(df_census_sex["TotalPop"]==0) & (df_census_sex["Women"] == 0)].groupby(["County","Borough"])["CensusTract"].count()
df_census_sex[(df_census_sex["TotalPop"]>0) & (df_census_sex["Women"] > 0)].groupby(["County","Borough"])["CensusTract"].count()
"""

# remove the non responses
df_census_sex = df_census_sex[(df_census_sex["TotalPop"]>0) & (df_census_sex["Women"] > 0)]

# limit dataset to only the locational information that we need
df_stations = df_stations[["Stop Name","GTFS Latitude","GTFS Longitude"]]

# create an array of coordinates for the reference stations that will be used in nearest neighbor function
station_array = df_stations[["GTFS Latitude","GTFS Longitude"]].values

# create an array of coordinates for the census data that will be used in nearest neighbor function
sex_array = df_census_sex[["Avg_Lat","Avg_Long"]].values

results = find_nearest(station_array,sex_array)

# copy the nearest neighbor indices into a column in the dataframe
df_census_sex['nearest_station_index'] = results

# check the kdtree result array 
df_stations.loc[results,:].head()

# create a merged dataframe that has info on Women counts + station location
df_station_sex = pd.merge(df_stations.reset_index(), df_census_sex, right_on="nearest_station_index", left_on="index", how='right')

# remove unneeded columns
df_station_sex.drop(columns=["index","Avg_Lat","Avg_Long","nearest_station_index"], inplace=True)

# add a column indicating the total count of women responding with respect to the nearest station
df_station_sex["Tot_Women_By_Station"] = df_station_sex.groupby(["Stop Name"])["Women"].transform(lambda x: sum(x))

# add a column indicating the total count of women responding to the survey overall
df_station_sex["Tot_Women"] = df_station_sex["Women"].sum()

# add a column which represents the percentage of women responding to the survey per closest station
df_station_sex["Women_Pct"] = (df_station_sex["Tot_Women_By_Station"]/df_station_sex["Tot_Women"])*100

# keep only one record per unique key of Stop Name, Station coordinates, Aggregated metrics
df_station_sex.drop_duplicates(["Stop Name"], keep = 'first', inplace = True)

df_station_sex_graph = df_station_sex[["Stop Name","GTFS Latitude","GTFS Longitude","Women_Pct","CensusTract"]].copy()

# identify the top 15 stations by percent of women responding to census, for use in a graph
df_station_top = df_station_sex_graph[['Stop Name','Women_Pct','CensusTract']].sort_values(by=['Women_Pct'], ascending=False).head(15)

# plot a horizontal bar graph with the top 15 stations by percent of women responding to census
categories = df_station_top['Stop Name']
values = df_station_top['Women_Pct']

plt.figure(dpi=100)

plt.barh(np.arange(len(categories)), values[::-1])

plt.yticks(np.arange(len(categories)),
           ['{}'.format(x) for x in categories[::-1]])

# save off the index to order other graphs in the same way 
df_station_top['new_index'] = df_station_top.reset_index().index

# repeat above steps again for other metrics - this would probably be better as a function
df_census_transit = df_census_merge[["CensusTract","County","Borough","TotalPop","Women","Transit","Avg_Lat","Avg_Long"]].copy()
df_census_empl = df_census_merge[["CensusTract","County","Borough","TotalPop","Women","Professional","Employed","Avg_Lat","Avg_Long"]].copy()

df_census_transit.dropna(axis=0, how='any',inplace=True)
df_census_empl.dropna(axis=0, how='any',inplace=True)

df_transit_merge = pd.merge(df_census_transit,df_station_top[["Stop Name","CensusTract","new_index"]],on='CensusTract')
df_empl_merge = pd.merge(df_census_empl,df_station_top[["Stop Name","CensusTract","new_index"]],on='CensusTract')

df_transit_top = df_transit_merge[df_transit_merge["Stop Name"].isin(df_station_top["Stop Name"].values)][["Stop Name","Transit","new_index"]].groupby(["Stop Name"]).mean().sort_values(by=["new_index"]).reset_index().head(15)
df_empl_top = df_empl_merge[df_empl_merge["Stop Name"].isin(df_station_top["Stop Name"].values)][["Stop Name","Professional","new_index"]].groupby(["Stop Name"]).mean().sort_values(by=["new_index"]).reset_index().head(15)

categories_transit = df_transit_top['Stop Name']
values_transit = df_transit_top['Transit']

plt.figure(dpi=100)

plt.barh(np.arange(len(categories_transit)),values_transit[::-1],color='orange')

plt.yticks(np.arange(len(categories_transit)),
           ['{}'.format(x) for x in categories_transit[::-1]])

categories_empl = df_empl_top['Stop Name']
values_empl = df_empl_top['Professional']

plt.figure(dpi=100)

plt.barh(np.arange(len(categories_empl)),values_empl[::-1],color='purple')

plt.yticks(np.arange(len(categories_empl)),
           ['{}'.format(x) for x in categories_empl[::-1]]);

# show metrics on same plot
station_top_list = df_station_top["Stop Name"].values.tolist()
transit_top_list = list(df_transit_top["Transit"].values)
empl_top_list = list(df_empl_top["Professional"].values)

df_station_metrics = pd.DataFrame(dict(graph=station_top_list,
                           transit=transit_top_list, 
                           empl=empl_top_list))

plt.figure(dpi=500)
ind = np.arange(len(df_station_metrics))
width = 0.4

fig, ax = plt.subplots()
ax.barh(ind, df_station_metrics.transit[::-1], width, color='orange', label='Transit')
ax.barh(ind - width, df_station_metrics.empl[::-1], width, color='purple', label='Professional')

ax.set(yticks=ind + width-0.5, yticklabels=df_station_metrics.graph[::-1], ylim=[2*width-1.5, len(df_station_metrics)-.6])
ax.legend()

