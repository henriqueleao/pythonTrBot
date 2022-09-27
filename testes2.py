from binance.client import Client
from binance.helpers import round_step_size
from decimal import *
from app.binance_functions import BinanceUtil


api_key = '009b0423e7f81c17ce24b1324c1f64e25e473f1f1e2dbb81c7b666483729203f'
api_secret = '7a6f7f1dfa2b1e418d39abaa77eca077362a8cb502aafd17915245393f65ec03'

binanceUtil = BinanceUtil(
    apiKey=api_key,
    secretKey=api_secret,
    testnet=True,
    percentualSizeTrade=10,
    leverage=10,
    concurrentTrades=5,
    useTrailing = True,
    callBackRate = 0.5,
    activationPerc = 1
)

binanceUtil.openLong('BTCUSDT',18500,20000)
