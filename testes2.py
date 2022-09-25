from binance.client import Client
from binance.helpers import round_step_size
from decimal import *

api_key = '009b0423e7f81c17ce24b1324c1f64e25e473f1f1e2dbb81c7b666483729203f'
api_secret = '7a6f7f1dfa2b1e418d39abaa77eca077362a8cb502aafd17915245393f65ec03'
client = Client(api_key, api_secret, testnet=True)
client.API_URL = 'https://testnet.binancefuture.com'
symbol = 'BTCUSDT'


def get_account_balance():
    balances = client.futures_account_balance()
    for balance in balances:
        if balance['asset'] == 'USDT':
            result = balance['balance']
    return float(result)


def get_min_quant(symbol):
    info = client.futures_exchange_info()
    for item in info['symbols']:
        if item['symbol'] == symbol:
            for f in item['filters']:
                if f['filterType'] == 'PRICE_FILTER':
                    return f['tickSize']


bet = 2  # the percentage of the balance I am willing to buy with
balance = get_account_balance() * bet / 100

tick_size = float(get_min_quant(symbol))
print(tick_size)

symbol_info = client.get_ticker(symbol=symbol)
symbol_price = float(symbol_info['lastPrice'])
#quantity = Decimal(round(balance / symbol_price,2))
quantity = Decimal(balance / symbol_price)

enter_long_coeff = 0.4
take_profit_percent = 0.2
stop_loss_percent = 0.2

price_long_enter = symbol_price * (1 - enter_long_coeff / 100)  # entry price for a limit order
price_long_enter = round_step_size(price_long_enter, tick_size)

take_profit_price = price_long_enter * (1 + take_profit_percent / 100)
take_profit_price = round_step_size(take_profit_price, tick_size)

stop_loss_price = price_long_enter * (1 + take_profit_percent / 100)
stop_loss_price = round_step_size(stop_loss_price, tick_size)

print(price_long_enter)
print(stop_loss_price)
print(take_profit_price)
print('=======')

limit_order_long = client.futures_create_order(
    symbol=symbol,
    side='BUY',
    positionSide='LONG',
    type='LIMIT',
    quantity=quantity,
    timeInForce='GTC',
    price=price_long_enter
)

sell_gain_market_long = client.futures_create_order(
    symbol=symbol,
    side='SELL',
    type='TAKE_PROFIT_MARKET',
    positionSide='LONG',
    quantity=quantity,
    stopPrice=take_profit_price
)

sell_stop_market_short = client.futures_create_order(
    symbol=symbol,
    side='SELL',
    type='STOP_MARKET',
    positionSide='LONG',
    quantity=quantity,
    stopPrice=stop_loss_price
)