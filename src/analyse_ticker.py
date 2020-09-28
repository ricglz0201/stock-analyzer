#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with functions for the analysis and further display
of the tickers
"""

from datetime import date, timedelta
from pandas.core.common import flatten
from tabulate import tabulate

from stock import Stock

# Time frame you want to pull data from
end = date.today()
start = end - timedelta(years=1)

all_data = []
averages = [20, 200]
overbought_data = []
oversold_data = []


def print_data(name, data):
    """
    Print in a certain format the data passed as an argument,
    alongside the associated name of the data
    """
    headers = flatten(['Stock', 'Price', 'RSI', 'MACD', 'chart'])
    print(name)
    print()
    print(tabulate(data, headers=headers))
    print()

def print_datas():
    """
    Print all the data in addition of those stocks that are
    overbought and oversold
    """
    print_data('All data', all_data)
    print_data('Overbought stocks', overbought_data)
    print_data('Oversold stocks', oversold_data)

def analyse_rsi(stock, data):
    """
    Performs analysis over the rsi of the stock and add the
    results in the analysis
    """
    current_rsi = float("{:.2f}".format(stock.rsi[-1]))
    is_overbought = current_rsi > 70
    is_oversold = current_rsi < 30
    current_rsi = str(current_rsi)

    if is_overbought:
        current_rsi += " 🔥"
    elif is_oversold:
        current_rsi += " 🧊"
    data.append(current_rsi)
    return is_overbought, is_oversold

def analyse_macd(stock, data):
    """
    Performs analysis over the macd of the stock and add the
    results in the analysis
    """
    current_macd = "{:.2f}".format(stock.macd[-1])
    if stock.is_currently_bullish():
        current_macd += " 🔥"
    else:
        current_macd += " 🧊"
    data.append(current_macd)

def analyse_ticker(ticker):
    """
    Performs reader for the corresponding ticker and checks
    if it's an actual rsi value for oversold or overbought
    """
    try:
        data = []

        print('Analysing data for {}'.format(ticker))

        stock = Stock(ticker, start, end)

        data.append(ticker.upper())

        data.append(stock.closes[-1])

        is_overbought, is_oversold = analyse_rsi(stock, data)
        analyse_macd(stock, data)

        chart_link = "https://finance.yahoo.com/quote/{0}/chart?p={0}".format(ticker)

        data.append(chart_link)

        if is_oversold:
            oversold_data.append(data)
            return stock
        if is_overbought:
            overbought_data.append(data)
        else:
            all_data.append(data)
        return None

    except Exception as error:
        print('Error: ', str(error), ticker)
