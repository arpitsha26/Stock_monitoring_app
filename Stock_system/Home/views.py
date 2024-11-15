from django.shortcuts import render
from django.http.response import HttpResponse
import yfinance as yf
import pandas as pd
import time
import queue
from threading import Thread

def lobby(request):
    return render(request, 'Home/lobby.html')


def stockpicker(request):
    symbols = ['MSFT', 'GOOGL', 'AMZN', 'TSLA']
    stockpicker = []
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        try:
            info = stock.info.get('symbol', symbol)  
            stockpicker.append(info)
        except Exception as e:
            print(f"Error for  {symbol}: {e}")
    return render(request, 'Home/stockpicker.html', {'stockpicker': stockpicker})


def stocktracker(request):
    selected_stocks = request.GET.getlist('stockpicker')
    data = {}
    for symbol in selected_stocks:
        stock = yf.Ticker(symbol)
        try:
            history = stock.history()  
            data[symbol] = history.to_dict('index') 
        except Exception as e:
            print(f"Error fetching history for {symbol}: {e}")
            data[symbol] = {"error": str(e)}

  
    return render(request, 'Home/stocktracker.html', {'data': data})