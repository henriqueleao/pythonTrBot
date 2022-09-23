import os
from dotenv import load_dotenv
from app.binance_functions import BinanceUtil

load_dotenv()
apiKey = os.environ.get('BINANCE_API_KEY')
secretKey = os.environ.get('BINANCE_SECRET_KEY')
testnet = True

bin = BinanceUtil(apiKey ,secretKey, testnet)
futures_account_balance = bin.client.futures_account_balance()

print ('ok')


