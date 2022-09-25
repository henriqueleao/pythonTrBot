import os
from dotenv import load_dotenv
from app.binance_functions import BinanceUtil
from binance import helpers

load_dotenv()
apiKey = os.environ.get('BINANCE_API_KEY')
secretKey = os.environ.get('BINANCE_SECRET_KEY')
testnet = True

bin = BinanceUtil(apiKey ,secretKey, testnet)
#futures_account_balance = bin.client.futures_account_balance()
symbol = 'BTCUSDT'
info = bin.client.get_symbol_info(symbol)
te

