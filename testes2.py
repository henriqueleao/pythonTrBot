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
def moeda_precisao(symbol):
    for x in client.futures_exchange_info()['symbols']:
        if x['symbol'] == symbol:
            return x['pricePrecision']
def get_step_size(symbol):
    info = client.futures_exchange_info()
    for item in info['symbols']:
        if item['symbol'] == symbol:
            for f in item['filters']:
                if f['filterType'] == 'LOT_SIZE':
                    return f['stepSize']

def get_tick_size(symbol):
    info = client.futures_exchange_info()
    for item in info['symbols']:
        if item['symbol'] == symbol:
            for f in item['filters']:
                if f['filterType'] == 'PRICE_FILTER':
                    return f['tickSize']

def testeOpenLong(symbol):
    bet = 2  # the percentage of the balance I am willing to buy with
    balance = get_account_balance() * bet / 100

    tick_size = float(get_tick_size(symbol))
    step_size = float(get_step_size(symbol))

    symbol_info = client.get_ticker(symbol=symbol)
    symbol_price = float(symbol_info['lastPrice'])

    qty_bruta = Decimal(balance/symbol_price)
    quantity = round_step_size(qty_bruta, step_size)

    take_profit_percent = 10
    stop_loss_percent = 5

    take_profit_price = (symbol_price * (100 + take_profit_percent))/100
    take_profit_price = round_step_size(take_profit_price, tick_size)

    stop_loss_price = (symbol_price * (100-stop_loss_percent))/100
    stop_loss_price = round_step_size(stop_loss_price, tick_size)

    client.futures_change_leverage(symbol=symbol, leverage=5)

    limit_order_long = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        #positionSide='LONG',
        type='MARKET',
        quantity=quantity
    )

    sell_gain_market_long = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='TAKE_PROFIT_MARKET',
        #positionSide='LONG',
        quantity=quantity,
        stopPrice=take_profit_price
    )

    sell_stop_market_short = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        type='STOP_MARKET',
        #positionSide='LONG',
        quantity=quantity,
        stopPrice=stop_loss_price
    )

def testeListTrades():
    futures_account = client.futures_account()
    openedPositions =[]
    for position in futures_account['positions']:
        if position['entryPrice'] != '0.0':
            openedPositions.append(position)
    print(openedPositions)

def testeOpenShort(symbol):
    bet = 2  # the percentage of the balance I am willing to buy with
    balance = get_account_balance() * bet / 100

    tick_size = float(get_tick_size(symbol))
    step_size = float(get_step_size(symbol))

    take_profit_percent = 10
    stop_loss_percent = 5

    symbol_info = client.get_ticker(symbol=symbol)
    symbol_price = float(symbol_info['lastPrice'])

    qty_bruta = Decimal(balance/symbol_price)
    quantity = round_step_size(qty_bruta, step_size)

    take_profit_price = (symbol_price * (100 - take_profit_percent))/100
    stop_loss_price = (symbol_price * (100+ stop_loss_percent))/100

    take_profit_price = round_step_size(take_profit_price, tick_size)
    stop_loss_price = round_step_size(stop_loss_price, tick_size)

    client.futures_change_leverage(symbol=symbol, leverage=5)

    market_order_short = client.futures_create_order(
        symbol=symbol,
        side='SELL',
        #positionSide='LONG',
        type='MARKET',
        quantity=quantity
    )

    sell_gain_market_short = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        type='TAKE_PROFIT_MARKET',
        quantity=quantity,
        stopPrice=take_profit_price
    )

    sell_stop_market_long = client.futures_create_order(
        symbol=symbol,
        side='BUY',
        type='STOP_MARKET',
        quantity=quantity,
        stopPrice=stop_loss_price
    )


testeOpenShort('ETHUSDT')