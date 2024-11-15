import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import yfinance as yf
from asgiref.sync import async_to_sync

STOCKS = ['AMZN', 'TSLA', 'GOOGL', 'MSFT',]
class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_stock_data()
        
    async def disconnect(self):
        pass
    
    
    async def receive(self, text_data):
        pass
        
    
    async def send_stock_data(self):
        stock_data = await self.fetch_stock_data()
        await self.send(json.dumps(stock_data))
    
    async def fetch_stock_data(self):
        stock_details= {}
        
        for ticker in STOCKS:
            stock = yf.Ticker(ticker)
            stock_info = stock.history(period="1d")
            current_price = stock.info.get('regularMarketPrice')
            stock_details[ticker] = {
                    "open": stock_info['Open'].iloc[-1],
                    "close": stock_info['Close'].iloc[-1],
                    "current_price": current_price, 
                }
        
        return stock_details
   