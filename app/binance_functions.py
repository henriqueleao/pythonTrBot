import os
import json
from binance.client import Client

class BinanceUtil:

    def __init__(self, apiKey, secretKey, testnet):
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.client = Client(self.apiKey, self.secretKey, testnet=testnet)
        self.client.API_URL = 'https://testnet.binance.vision/api'
        self.concurrentTrades = 5






