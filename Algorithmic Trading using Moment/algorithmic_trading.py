# -*- coding: utf-8 -*-
"""Algorithmic Trading.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LSu3XS3y9XVfJgfUZ4IjXvcdv_oyPgIk

# Algorithmic Trading in Python

In this section, I will implement an Algorithm Trading strategy known as the momentum strategy on stock price data using Python. In the momentum strategy, we buy the stocks when the momentum is positive and sell the stocks when the momentum is negative.
"""

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import yfinance as yf

# Get Apple's stock data from yahoo finance
stock = yf.Ticker("AAPL")
data = stock.history(period="1y")
print(data.head())

"""Now let’s implement the momentum strategy in Algorithmic Trading using Python:"""

# Calculation of momentum
data['momentum'] = data['Close'].pct_change()

# Creating subplots to show momentum and buying/selling markers
figure = make_subplots(rows=2, cols=1)
figure.add_trace(go.Scatter(x=data.index, 
                         y=data['Close'], 
                         name='Close Price'))
figure.add_trace(go.Scatter(x=data.index, 
                         y=data['momentum'], 
                         name='Momentum', 
                         yaxis='y2'))

# Adding the buy and sell signals
figure.add_trace(go.Scatter(x=data.loc[data['momentum'] > 0].index, 
                         y=data.loc[data['momentum'] > 0]['Close'], 
                         mode='markers', name='Buy', 
                         marker=dict(color='green', symbol='triangle-up')))

figure.add_trace(go.Scatter(x=data.loc[data['momentum'] < 0].index, 
                         y=data.loc[data['momentum'] < 0]['Close'], 
                         mode='markers', name='Sell', 
                         marker=dict(color='red', symbol='triangle-down')))

figure.update_layout(title='Algorithmic Trading using Momentum Strategy',
                  xaxis_title='Date',
                  yaxis_title='Price')
figure.update_yaxes(title="Momentum", secondary_y=True)
figure.show()

"""Algorithmic Trading means using algorithms in buying and selling decisions in the financial market. In an algorithmic trading strategy, a set of predefined rules are used to determine when to buy a financial instrument and when to sell it."""