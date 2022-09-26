import os
import json
from binance.client import Client
from decimal import *
from binance.helpers import round_step_size

class BinanceUtil:

    def __init__(self, apiKey, secretKey, testnet, leverage, concurrentTrades, percentualSizeTrade):
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.client = Client(self.apiKey, self.secretKey, testnet=testnet)
        if testnet:
            self.client.API_URL = 'https://testnet.binance.vision/api'
        self.percentualSizeTrade = percentualSizeTrade
        self.concurrentTrades = concurrentTrades
        self.leverage = leverage

    def get_account_balance(self, asset):
        balances = self.client.futures_account_balance()
        for balance in balances:
            if balance['asset'] == asset:
                result = balance['balance']
        return float(result)

    def get_step_size(self, symbol):
        info = self.client.futures_exchange_info()
        for item in info['symbols']:
            if item['symbol'] == symbol:
                for f in item['filters']:
                    if f['filterType'] == 'LOT_SIZE':
                        return f['stepSize']

    def get_tick_size(self, symbol):
        info = self.client.futures_exchange_info()
        for item in info['symbols']:
            if item['symbol'] == symbol:
                for f in item['filters']:
                    if f['filterType'] == 'PRICE_FILTER':
                        return f['tickSize']

    def get_list_trades(self):
        futures_account = self.client.futures_account()
        openedPositions = []
        for position in futures_account['positions']:
            if position['entryPrice'] != '0.0':
                openedPositions.append(position)
        return (openedPositions)

    def openLong(self, symbol, stopLossPrice, takeProfitPrice):
        balance = self.get_account_balance(asset='USDT') * self.percentualSizeTrade / 100
        self.client.futures_change_leverage(symbol=symbol, leverage=self.leverage)
        tick_size = float(self.get_tick_size(symbol))
        step_size = float(self.get_step_size(symbol))
        symbol_info = self.client.get_ticker(symbol=symbol)
        symbol_price = float(symbol_info['lastPrice'])
        qty_bruta = Decimal(balance / symbol_price)
        quantity = round_step_size(qty_bruta, step_size)

        take_profit_price = round_step_size(takeProfitPrice, tick_size)
        stop_loss_price = round_step_size(stopLossPrice, tick_size)
        market_order_long = self.client.futures_create_order(
            symbol=symbol,
            side='BUY',
            type='MARKET',
            quantity=quantity
        )

        sell_gain_market_long = self.client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='TAKE_PROFIT_MARKET',
            quantity=quantity,
            stopPrice=take_profit_price
        )

        sell_stop_market_short = self.client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='STOP_MARKET',
            quantity=quantity,
            stopPrice=stop_loss_price
        )

    def openShort(self, symbol, leverage, stopLossPrice, takeProfitPrice):
        balance = self.get_account_balance(asset='USDT') * self.percentualSizeTrade / 100
        self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
        tick_size = float(self.get_tick_size(symbol))
        step_size = float(self.get_step_size(symbol))
        symbol_info = self.client.get_ticker(symbol=symbol)
        symbol_price = float(symbol_info['lastPrice'])
        qty_bruta = Decimal(balance / symbol_price)
        quantity = round_step_size(qty_bruta, step_size)

        take_profit_price = round_step_size(takeProfitPrice, tick_size)
        stop_loss_price = round_step_size(stopLossPrice, tick_size)

        market_order_short = self.client.futures_create_order(
            symbol=symbol,
            side='SELL',
            type='MARKET',
            quantity=quantity
        )

        sell_gain_market_short = self.client.futures_create_order(
            symbol=symbol,
            side='BUY',
            type='TAKE_PROFIT_MARKET',
            quantity=quantity,
            stopPrice=take_profit_price
        )

        sell_stop_market_long = self.client.futures_create_order(
            symbol=symbol,
            side='BUY',
            type='STOP_MARKET',
            quantity=quantity,
            stopPrice=stop_loss_price
        )