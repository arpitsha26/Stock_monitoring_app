import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import yfinance as yf
from asgiref.sync import sync_to_async
from .models import Stock


class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "Connected successfully"}))
        asyncio.create_task(self.send_user_subscribed_stocks())

    async def disconnect(self, code):
       
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        stocks = data.get("stocks", [])

        if action == "subscribe":
            await self.send(json.dumps({"message": f"Subscribed to {stocks}."}))
        elif action == "unsubscribe":
            await self.send(json.dumps({"message": f"Unsubscribed from {stocks}."}))
        else:
            await self.send(json.dumps({"error": "Invalid action"}))

    async def send_user_subscribed_stocks(self):
        while True:
            stock_data = await self.fetch_stock_data()
            await self.send(json.dumps(stock_data))
            await asyncio.sleep(20)

    async def fetch_stock_data(self):
        stock_symbols = ["MSFT", "GOOGL", "AAPL"]
        stock_details = {}

        for ticker in stock_symbols:
            try:
                stock = yf.Ticker(ticker)
                current_price = stock.info.get("regularMarketPrice", None)

                if current_price is None:
                    history = stock.history(period="1d")
                    close_price = history["Close"].iloc[-1] if not history.empty else "N/A"
                    current_price = close_price

                stock_details[ticker] = {"current_price": current_price}
            except Exception as e:
                stock_details[ticker] = {"error": f"Error fetching data: {str(e)}"}

        return stock_details
