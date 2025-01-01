# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 17:25:37 2024

@author: sdhan
"""

import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Set date range for data
end_date = dt.date.today()  # End date is the current date
start_date = end_date - dt.timedelta(days=500)  # Start date is 500 days before the end date

# Download stock data
stocks = ['ABB.NS','ADANIENSOL.NS','ADANIENT.NS','ADANIGREEN.NS','ADANIPORTS.NS','ADANIPOWER.NS','ATGL.NS','AMBUJACEM.NS','APOLLOHOSP.NS','ASIANPAINT.NS','DMART.NS','AXISBANK.NS','BAJAJ-AUTO.NS','BAJFINANCE.NS','BAJAJFINSV.NS','BAJAJHLDNG.NS','BANKBARODA.NS','BEL.NS','BHEL.NS','BPCL.NS','BHARTIARTL.NS','BOSCHLTD.NS','BRITANNIA.NS','CANBK.NS','CHOLAFIN.NS','CIPLA.NS','COALINDIA.NS','DLF.NS','DABUR.NS','DIVISLAB.NS','DRREDDY.NS','EICHERMOT.NS','GAIL.NS','GODREJCP.NS','GRASIM.NS','HCLTECH.NS','HDFCBANK.NS','HDFCLIFE.NS','HAVELLS.NS','HEROMOTOCO.NS','HINDALCO.NS','HAL.NS','HINDUNILVR.NS','ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','ITC.NS','IOC.NS','IRCTC.NS','IRFC.NS','INDUSINDBK.NS','NAUKRI.NS','INFY.NS','INDIGO.NS','JSWENERGY.NS','JSWSTEEL.NS','JINDALSTEL.NS','JIOFIN.NS','KOTAKBANK.NS','LTIM.NS','LT.NS','LICI.NS','LODHA.NS','M&M.NS','MARUTI.NS','NHPC.NS','NTPC.NS','NESTLEIND.NS','ONGC.NS','PIDILITIND.NS','PFC.NS','POWERGRID.NS','PNB.NS','RECLTD.NS','RELIANCE.NS','SBILIFE.NS','MOTHERSON.NS','SHREECEM.NS','SHRIRAMFIN.NS','SIEMENS.NS','SBIN.NS','SUNPHARMA.NS','TVSMOTOR.NS','TCS.NS','TATACONSUM.NS','TATAMOTORS.NS','TATAPOWER.NS','TATASTEEL.NS','TECHM.NS','TITAN.NS','TORNTPHARM.NS','TRENT.NS','ULTRACEMCO.NS','UNIONBANK.NS','UNITDSPR.NS','VBL.NS','VEDL.NS','WIPRO.NS','ZOMATO.NS','ZYDUSLIFE.NS']  # List of stock tickers
# stocks = ['ABB.NS']  # Uncomment for debugging with a single stock

difference = []  # To store percentage differences between high and recent low
Ascending_triangle = []  # To store differences for Ascending Triangle patterns

for stock in stocks:
    # Download historical stock data for each ticker
    data = yf.download(stock, start=start_date, end=end_date, interval="1D")
    data = np.round(data, 2)  # Round data to 2 decimal places for consistency

    # Calculate the highest value (High) of the stock
    High = data["High"].max()

    # Calculate the difference between the highest value and the first low value
    best = High - data["Low"].iloc[1]
    Ascending_triangle.append(best)  # Store the result

    # Calculate percentage difference between highest value and the most recent low value
    diff = (High - data["Low"].iloc[-1]) / data["Low"].iloc[-1]
    difference.append(diff)  # Append the difference to the list

# Convert differences into a Pandas Series for sorting
difference = pd.Series(difference, index=stocks)

# Sort stocks by their calculated differences
values = difference.sort_values(ascending=True)

# Extract the stock names from sorted values
stock_name = values.index
print("\n------------------------------")
print("Stocks with the Ascending Triangle Pattern")
print(stock_name[1:5])  # Print the top 4 stocks with potential patterns

# Select the best stock based on calculated differences
best_ascending_triangle = stock_name[1]

# Download data for the best stock
stock_data = yf.download(best_ascending_triangle, start=start_date, end=end_date, interval="1D")

# Find the lowest value and the date of occurrence in the stock data
Low = stock_data["Low"].min()
Low_date = stock_data["Low"].idxmin()  # Date when the minimum occurs
Low_position = stock_data.index.get_loc(Low_date)  # Position of the lowest value

# Extract the most recent low value
low1 = stock_data["Low"].iloc[-1]

# Calculate positions for plotting lines
a = len(stock_data) - Low_position  # Position of the lowest point relative to the end
b = 1  # Position of the most recent data point

# Find the highest value of the stock
High = stock_data["High"].max()

# Create two points for the ascending triangle pattern
two_points = [[(stock_data.index[-a], stock_data["Low"].iloc[-a]),
               (stock_data.index[-b], stock_data["Low"].iloc[-b])]]

# Create figure and axis
fig = figsize = (16, 10)

# Plot the candlestick chart with ascending triangle pattern
mpf.plot(stock_data, type='candle', style='charles', hlines=High, alines=two_points, volume=False, 
         title=f'{best_ascending_triangle} Stock with Ascending Triangle')

# Show the plot
plt.show()
