from django.shortcuts import render
from django.http.response import HttpResponse
import yfinance as yf

import time
import queue

def lobby(request):
    return render(request, 'Home/lobby.html')


def stockpicker(request):
    stock_picker = yf.Tickers('msft aapl goog')

    print(stock_picker)
    return render(request,'Home/stockpicker.html',  {'stockpicker':stock_picker})

def stocktracker(request):
    return render(request,'Home/stocktracker.html' )