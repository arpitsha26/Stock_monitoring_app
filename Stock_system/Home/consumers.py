from channels.generic.websocket import WebsocketConsumer
import json

class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({'status': 'connected'}))
