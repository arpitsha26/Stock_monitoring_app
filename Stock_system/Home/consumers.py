import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import yfinance as yf
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import User, Stock

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
            self.user = user
            await self.accept()
            await self.send(json.dumps({"mssg": "connected ok"}))
            asyncio.create_task(self.send_user_subscribed_stocks())
        else:
            await self.close()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope["user"]

        if user.is_authenticated:
            action = data.get("action")
            stocks = data.get("stocks", [])
            if action == "subscribe":
                await sync_to_async(self.subscribe_to_stocks)(stocks)
                await self.send(json.dumps({"mssg": f"subscribed to {stocks}."}))
            if action == "unsubscribe":
                await sync_to_async(self.unsubscribe_from_stocks)(stocks)
                await self.send(json.dumps({"mssg": f"unsubscribe from {stocks}."}))
        else:
            await self.send(json.dumps({"eror": "not authenticated user"}))

    async def send_user_subscribed_stocks(self):
        while True:
            stock_data = await self.fetch_stock_data()
            await self.send(json.dumps(stock_data))
            await asyncio.sleep(20)

    async def fetch_stock_data(self):
        user_stocks = await sync_to_async(self.get_user_stocks)()
        stock_details = {}

        for ticker in user_stocks:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.history(period="1d")
                current_price = stock.info.get("regularMarketPrice")
                stock_details[ticker] = {"current_price": current_price}
            except Exception as e:
                stock_details[ticker] = {"error": f"error in fetcing: {str(e)}"}

        return stock_details

    def get_user_stocks(self):
        return list(self.user.subscribed_stocks.values_list("symbol", flat=True))

    def subscribe_to_stocks(self, stocks):
        available_stocks = list(
            Stock.objects.filter(symbol__in=stocks).values_list("id", flat=True)
        )
        self.user.subscribed_stocks.add(*available_stocks)

    def unsubscribe_from_stocks(self, stocks):
        stocks_to_remove = Stock.objects.filter(symbol__in=stocks)
        self.user.subscribed_stocks.remove(*stocks_to_remove)
