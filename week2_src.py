import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
from datetime import date
import numpy as np
%matplotlib notebook
import matplotlib.dates as dates
import matplotlib.ticker as ticker

#reading data
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

#data preprocessing

#convert temperature to degree Celcius
df['Data_Value'] = df['Data_Value']*0.1
#convert date to datetime format
df['Date'] = pd.to_datetime(df['Date'])

#removing Feb 29th
df['Month_Date'] = df['Date'].dt.strftime('%m-%d')
df = df[df['Month_Date'] != '02-29']

df['year'] = df['Date'].dt.year

filtered_df_min = df[(df['Element']=='TMIN') & (df['year'] >= 2005) & (df['year']<2015)].groupby(['Month_Date'])['Data_Value'].min()
filtered_df_max = df[ (df['year'] >= 2005) & (df['year']<2015) & (df['Element']=='TMAX')].groupby(['Month_Date'])['Data_Value'].max()

df = df.merge(filtered_df_min.reset_index(drop=False).rename(columns={'Data_Value':'Min_temp'}), on='Month_Date', how='left')
df = df.merge(filtered_df_max.reset_index(drop=False).rename(columns={'Data_Value':'Max_temp'}), on='Month_Date', how='left')

#finding records that surpassed max and min temperatures in 2015
record_high = df[(df.year==2015) & (df.Data_Value > df.Max_temp)]
record_low = df[(df.year==2015) & (df.Data_Value < df.Min_temp)]


#plotting
# X Axis spanning 2015 only:
date_index = np.arange('2015-01-01','2016-01-01', dtype='datetime64[D]')

plt.figure()
plt.title('Line graphs representing max & min temperatures in (2005-2014) and the scatter plot to display ')
plt.plot(date_index,filtered_df_max,color='lightcoral',linewidth=1)
plt.plot(date_index,filtered_df_min,color='skyblue',linewidth=1)

#including the scatter plot for 2015
plt.scatter(record_high.Date.values, record_high.Data_Value.values,color='red',s=5)
plt.scatter(record_low.Date.values, record_low.Data_Value.values,color='blue',s=5)

#setting limits for x and y axes
ax = plt.gca()
ax.axis(['2015-01-01','2015-12-31',-50,50])

plt.xlabel('Date')
plt.ylabel('Temperature in Degree Celcius')
plt.title('Reported Temperatures distibution between 2005 and 2015')
plt.legend(['Max temp (2005-2014)','Min temp (2005-2014)','2015 Max Temp','2015 Min Temp'],loc=0,frameon=False)
#filling area between the graphs
plt.gca().fill_between(date_index,filtered_df_max,filtered_df_min,facecolor='grey',alpha=0.25)

ax.xaxis.set_major_locator(dates.MonthLocator())
ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15))

ax.xaxis.set_major_formatter(ticker.NullFormatter())
ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.label1.set_horizontalalignment('center')
    
plt.show()