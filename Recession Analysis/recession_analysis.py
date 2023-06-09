# -*- coding: utf-8 -*-
"""RECESSION ANALYSIS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JlIK1zzaFy_q6RcOsTSf9l22GM8_6Rw8

#Recession Analysis

Recession is calculated and analyzed according to the growth in GDP, the growth in the unemployment rate, and the growth in consumer spending rate. But the most common way of measuring recession is by analyzing the monthly GDP growth data.

So, for the task of Recession analysis, we need to have a dataset of the monthly GDP growth of a country. I found an ideal dataset for this task that is based on the monthly GDP growth rate of the United Kingdom. You can download the dataset from here.
"""

import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_white"

data = pd.read_csv('UK_monthly_gdp.csv')
print(data.head())

"""Let’s have a look at the GDP growth over time:"""

fig = go.Figure(data=go.Heatmap(
                   z=[data['GDP Growth']],
                   x=data.index,
                   y=['GDP Growth'],
                   colorscale='Viridis'))

fig.update_layout(title='GDP Growth over Time',
                  xaxis_title='Time Period',
                  yaxis_title='')

fig.show()

"""As a recession means the decline in the circulation of money for two consecutive quarters, I will convert our monthly data into quarterly data to analyze the recession:"""

# Convert monthly data to quarterly data using resample method
data['Time Period'] = pd.to_datetime(data['Time Period'], format='/%m/%Y')
data.set_index('Time Period', inplace=True)
quarterly_data = data.resample('Q').mean()
print(quarterly_data.head())

"""Now here’s how we can calculate and analyze recession based on quarterly GDP growth:"""

# Calculate recession based on quarterly GDP growth
quarterly_data['Recession'] = ((quarterly_data['GDP Growth'] < 0) & (quarterly_data['GDP Growth'].shift(1) < 0))

# Fill missing values with False (since the first quarter cannot be in a recession)
quarterly_data['Recession'].fillna(False, inplace=True)

# Plot the GDP growth and recession data
fig = go.Figure()
fig.add_trace(go.Scatter(x=quarterly_data.index, 
                         y=quarterly_data['GDP Growth'], 
                         name='GDP Growth', 
                         line=dict(color='green', width=2)))
fig.add_trace(go.Scatter(x=quarterly_data[quarterly_data['Recession']].index, 
                         y=quarterly_data[quarterly_data['Recession']]['GDP Growth'], 
                         name='Recession', line=dict(color='red', width=2)))

fig.update_layout(title='GDP Growth and Recession over Time (Quarterly Data)',
                  xaxis_title='Time Period',
                  yaxis_title='GDP Growth')

fig.show()

"""The red line shows the periods of negative GDP growth (considered recessions), and the green line shows the overall trend in GDP growth over time.

Let us now analyze the severity of the recession. The severity of a recession refers to the extent to which the economy contracts during a recession. A severe recession involves a deeper and more prolonged decline in economic activity, resulting in negative effects on employment, incomes and other economic indicators. Here’s how to analyze the severity of the recession:
"""

quarterly_data['Recession Start'] = quarterly_data['Recession'].ne(quarterly_data['Recession'].shift()).cumsum()
recession_periods = quarterly_data.groupby('Recession Start')
recession_duration = recession_periods.size()
recession_severity = recession_periods['GDP Growth'].sum()

fig = go.Figure()
fig.add_trace(go.Bar(x=recession_duration.index, y=recession_duration,
                     name='Recession Duration'))
fig.add_trace(go.Bar(x=recession_severity.index, y=recession_severity,
                     name='Recession Severity'))

fig.update_layout(title='Duration and Severity of Recession',
                  xaxis_title='Recession Periods',
                  yaxis_title='Duration/Severity')

fig.show()