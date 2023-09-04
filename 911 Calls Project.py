import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
os.chdir(r'C:\Users\Lenovo\Desktop\Python Bootcamp\10-Data-Capstone-Projects')
df = pd.read_csv('911.csv')

# Basic questions
 # Top 5 zip codes and townships for 911 calls
df['zip'].value_counts().head()
df['twp'].value_counts().head()
 # Number of unique title codes
df['title'].nunique()

# Creating new features
 # The most common reasons call for 911
df['Reason'] = df['title'].apply(lambda x: x.partition(':')[0])
df['Reason'].value_counts()
 # A count plot of 911 calls 
sns.countplot(x= df['Reason'])
 # The data type of the objects in the Timestamp column 
empty_set = set()
for i in df['timeStamp']:
    empty_set.add(type(i))
print(empty_set)
 # Converting the objects to Datetime objects
df['timeStamp'] = pd.to_datetime(df['timeStamp'])
df['Hour'] = df['timeStamp'].dt.hour
df['Month'] = df['timeStamp'].dt.month
df['Day of Week'] = df['timeStamp'].dt.day_name()
df
 # A countplot for Day of Week and Month with the hue based off the Reason column
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12, 4))
sns.countplot(x = df['Day of Week'], hue = df['Reason'], ax = ax1)
sns.countplot(x = df['Month'], hue = df['Reason'], ax = ax2)
 # Still some months are missing, we need to fill in this information
month_obj = df.groupby('Month')
month_obj.count().head()
 # A plot indicating the counts of call per month
month_obj.count()['lat'].plot() # A simple line plot
 # A linear fit of the number of calls per month by using seaborn sns' lmplot
sns.lmplot(x = 'Month', y = 'lat', data = month_obj.count().reset_index())
 # A plot indicating the counts of call per day
df['Date'] = df['timeStamp'].dt.date
date_obj = df.groupby('Date')
date_obj.count()['lat'].plot()
 # 3 separate plots with each plot representing a Reason for the 911 call
def string_value(x: str):
    mt = []
    for i in range(len(x)):
        mt.append(ord(x[i]))
    return sum(mt)

comparison = np.vectorize(string_value)
better_df = df.sort_values(by = 'Reason', key = comparison)
outside = better_df['Reason']
inside = better_df['Date']
hier_index = list(zip(outside, inside))
multi_index = pd.MultiIndex.from_tuples(hier_index)
call_for_EMS = better_df.set_index(multi_index).loc['EMS']
call_for_Fire = better_df.set_index(multi_index).loc['Fire']
call_for_Traffic = better_df.set_index(multi_index).loc['Traffic']
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (12, 12))
 # pd.Series.plot(kind = , xlabel=, ylabel =,  **kwargs from the plt.plot() function)
call_for_EMS.groupby('Date').count()['lat'].plot(ax = ax1, color = 'blue', ylabel = 'Calls')
call_for_Fire.groupby('Date').count()['lat'].plot(ax = ax2, color = 'red', ylabel = 'Calls')
call_for_Traffic.groupby('Date').count()['lat'].plot(ax = ax3, color = 'green', ylabel = 'Calls')
ax1.set_title('EMS')
ax2.set_title('Fire')
ax3.set_title('Traffic')
plt.subplots_adjust(hspace= 1)
 # Restructure the data frame so that the columns become the Hours and the index becomes the Day of Week by using "df.groupby()" and "pd.DataFrame.unstack(level = -1, fill_value = None)". This method will return a DataFrame having a new level of column labels whose inner-most level consists of the pivoted index labels. If the index is not a Multiindex, the output will be a Series
  # level: "int" or "list of ints" is level(s) of index to unstack
  # fill_value: "int", "str" or "dict" to replace NaN with this value if they exist
hour_df = df.groupby(['Day of Week', 'Hour']).count()['lat'].unstack()
 # A heatmap of this DataFrame
sns.heatmap(hour_df, cmap = 'viridis')
 # A clustermap of this DataFrame
sns.clustermap(hour_df, cmap = 'viridis')
 # Do the same operations, this time for a DataFrame with the columns as Months
month_df = df.groupby(['Day of Week', 'Month']).count()['lat'].unstack(level = -1)
sns.heatmap(month_df)
sns.clustermap(month_df)
 
# Recalled concepts
 # Data Frames, Series, Operations, Groupby
 # Built-in Data Visualization with Pandas
 # plt.subplots(), ax.spines[''].set_color(), ax.xaxis.tick_left(), plt.subplots_adjust(hspace =, wspace =, left =, right =, bottom =, top =)
 # Matrix and Regression plots in Seaborn, pd.Series.plot(kind = , ax =, xlabel=, ylabel =, xticks =, yticks =, *kwargs in plt.plot())

# Additional lessons learned: 
 # pd.to_datetime(arg): this function converts a scalar, array_like, Series or DataFrames/dict-like to Pandas datetime object
 # Common Datetime Accessors to extract in Pandas
  # dt.week (the week number)
  # dt.year (the year value as an integer)
  # dt.date (date without time values)
  # dt.day (the day of the month as value from 1 through 31)
  # dt.month (the month of the year as value from 1 through 12)
  # dt.weekday (the day of week returned as a value where Monday = 0 and Sunday = 6)
  # dt.day_name() (the name of the weekday return as a string)

 # We can access the names of the colormaps by using "plt.colormaps()"
 
# Especially useful tools for:
 # Counting: "df.groupby().count()", which is a DataFrame and then we can access the columns accordingly
 # "The most common": df[''].value_counts() (which is also a DataFrame)