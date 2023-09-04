from pandas_datareader import data
import cufflinks as cf
import pandas as pd
import seaborn as sns
import yfinance as yfin
import matplotlib.pyplot as plt
import datetime
sns.set_style('whitegrid')
cf.go_offline()
yfin.pdr_override() # Make Pandas Datareader optional

# Ticker symbols are just a shorthand way of describing a company's stock. They are unique series of letters assigned to a security for trading purposes.
 # Bank of America: BAC
 # CitiGroup: C
 # Goldman Sachs: GS
 # JPMorgan Chase: JPM
 # Morgan Stanley: MS
 # Wells Fargo: WFC
 
start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)

BAC = data.get_data_yahoo('BAC', start, end)
C = data.get_data_yahoo('C', start, end)
GS = data.get_data_yahoo('GS', start, end)
JPM = data.get_data_yahoo('JPM', start, end)
MS = data.get_data_yahoo('MS', start, end)
WFC = data.get_data_yahoo('WFC', start, end)

tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']
bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC], keys = tickers, axis =1)
# pd.concat(obj, axis = 0, join = 'outer', ignore_index = False, keys = None, levels = None)
 # keys = sequence: Construct hierarchical index using the passed keys as the outermost level
 # levels = list/sequence: Specific levels (unique values) to use for constructing a Multiindex. Otherwise they will be inferred from the keys.
bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']

# Exploratory Data Analysis (EDA)

 # What is the max Close price for each bank's stock through out the time period
bank_stocks.xs('Close', axis = 1, level = 'Stock Info').max().transpose()

 # Create a "Returns" DataFrame, which will contain the "return" for each bank's stocks. The "total" return for a stock includes both "capital gains/losses" and "dividend income" while the "nominal return" for a stock only depicts its price change.
  # The term capital gain refers to the increase in the value of a capital asset when it is sold like a stock, real estate, etc.
  # A dividend is a cash payment that companies pay to their shareholders. It's a way that businesses return extra profits to their owners.
returns = pd.DataFrame()
for i in range(len(tickers)):
    returns['{} Return'.format(tickers[i])] = bank_stocks.xs('Close', axis = 1, level = 'Stock Info')[tickers[i]].pct_change()
  # pd.Series.pct_change(periods = 1, ffill = 'pad', limit = None)
   # "periods" is the Periods to shift for forming percent change
   # "fill_method" and "limit" are arguments in the "df.fillna()"
   
 # Create a Pairplot of the "returns" DataFrame
sns.pairplot(returns)
  # What stocks stand out for you? (See solutions later)

 # Figure out on what dates each bank stock had the best and worst single day returns?
returns.idxmax()
returns.idxmin()
  # 4 banks share the same worst single day returns, which happens to be 20/1/2009 - the day that Barack Obama is inaugurated as the 44th President of the United States
  # CityGroup's biggest gain and largest drop days were very close from each other (24/11/2008 - 27/2/2009), during which the recession after the 2008 Financial Crisis started.
  
 # Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015?
  # A high standar deviation shows that the data is widely spread (less reliable) and a low standard deviation shows that the data are clustered closely around the mean (more reliable)
returns.std()
 # The stock of CityGroup bank is the riskiest over the entire time period
returns['date'] = pd.to_datetime(returns.index)
returns['Year'] = returns['date'].dt.year
multi_index = pd.MultiIndex.from_tuples(list(zip(returns['Year'], returns['date'])))
returns.set_index(multi_index, inplace = True)
returns.xs(('2015, ')).std()
 # The Morgan Stanley's stocks are the riskiest of the year 2015  
 
 # Create displots using Seaborn of the 2015 returns for Stanley and the 2008 returns for CityGroup
sns.displot(returns.xs(('2015, '))['MS Return'], kde = True)
sns.distplot(returns.xs(('2008, '))['C Return'], kde = True, color = 'red')

# More visualization
 # A line plot showing Close price for each bank through the entire index of time
for tick in tickers:
  bank_stocks[tick]['Close'].plot(figsize = (12, 4), label = tick)
  
bank_stocks.xs('Close', axis = 1, level = 'Stock Info').plot()

bank_stocks.xs('Close', axis = 1, level = 'Stock Info').iplot()

# Moving averages for stocks in the year 2008
fig, ax = plt.subplots(figsize = (12, 4))
bank_stocks['BAC']['Close'].loc['2008-01-01':'2009-01-01'].rolling(window = 30).mean().plot(ax = ax, label = '30 Days Average')
bank_stocks['BAC']['Close'].loc['2008-01-01':'2009-01-01'].plot(ax = ax, label = 'BAC CLOSE')
plt.legend(loc = 'upper right')
 # pd.DataFrame/Series.rolling(window = , on = None, axis = 0, closed = 'right' , method = 'single', step = None) provides rolling window calculations.
  # "window = int": the size of the moving window
  # "on = str": For a DataFrame, a column label or index level on which to calculate the rolling window, rather than the DataFrame's index
  # "axis = 0": roll across the rows. If 1, roll across the columns (for Series, this parameter is unused)
  # "closed = 'right'/'left'/'both'/neither'". The first, the last, the no, the first and last points in the window are excluded from calculations
  # "method = 'single'/'table'": execute the rolling operation per single column/row or over the entire object
  # "step = int": evaluate the window at every step result.
# Rolling window calculations involve taking subsets of data, where subsets are of the same or varying length and performing mathematical calculations on them.

# Create a heatmap of the correlation between the stocks' close price
sns.heatmap(bank_stocks.xs('Close', axis = 1, level = 'Stock Info').corr(), cmap = 'RdBu', annot = True)

# Use the clustermap to cluster the correlations together
sns.clustermap(bank_stocks.xs('Close', axis = 1, level = 'Stock Info').corr(), cmap = 'RdBu', annot = True)

# Recalled concepts:
 # Combining DataFrames 
 # Missing Data
 # Seaborn Grids, Style and Colors
 # Seaborn Distribution plots
 
# Additional lessons learned:
 # Advanced indexing with hierarchical index
 # pd.Series/DataFrame.rolling()
