import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import math

#Reading stock data from CSV file
data = pd.read_csv("TSLA1516.csv")
data['Date'] = pd.to_datetime(data['Date'], format = '%Y-%m-%d')
data.set_index(['Date'], inplace=True)

#Calculating the daily log returns
pct_daily_return = data['Adj Close'].pct_change()
log_daily_return = np.log(1 + pct_daily_return)

#Calculating the average, variance and standard deviation of the daily log returns and then finding the drift.
average_daily_return = log_daily_return.mean()
variance = log_daily_return.var()
standard_deviation = log_daily_return.std()
drift = average_daily_return - (variance/2)

print("Average Daily Return: " + str(average_daily_return))
print("Variance: " + str(variance))
print("Standard Deviation: " + str(standard_deviation))
print("Drift: " + str(drift))

#How many simulations we want for how many days
num_simulations = 10
num_days = 60

#List to store the data from all simulations
all_stats = []

#Calculate the possible forecasted prices
for i in range(num_simulations):
    today_price = data['Adj Close'].iloc[-1]
    day_prices = []
    for j in range(num_days):
        random_value = standard_deviation * norm.rvs()
        next_day_price = today_price * math.exp(drift + random_value)
        day_prices.append(next_day_price)
        today_price = next_day_price

    all_stats.append(day_prices)

#Calculate the median for each day
median_array = []
for i in range(num_days):
    temp_array = []
    for j in range(num_simulations):
        temp_array.append(all_stats[j][i])

    median_array.append(np.median(temp_array))

#Plot the graph
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])

for x in range(num_simulations):
    ax1.plot(all_stats[x])

ax1.plot(median_array, 'bo')

ax1.set_xlabel("Days From Last Record")
ax1.set_ylabel("Forecasted Adj. Closing Price")
ax1.set_title("Forecasted Adj. Closing Prices")
plt.show()




