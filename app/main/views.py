from . import main
import traceback
import json, os
from flask import request, abort
from ..binance_functions import BinanceUtil

@main.route('/')
def index():
    return 'Trading Bot1 - teste'

@main.route('/testeBinance', methods=['POST'])
def testeBinance():
    binanceUtil = BinanceUtil(
        apiKey=os.environ.get('BINANCE_API_KEY'),
        secretKey=os.environ.get('BINANCE_SECRET_KEY'),
        testnet=os.environ.get('TESTNET'),
    )
    return str(binanceUtil.get_account_balance('USDT'))


@main.route('/webhook_testnet', methods=['POST'])
def webhook_testnet():
    data = json.loads(request.data)
    if data['pwd'] != os.environ.get('WEBHOOK_PASSPHRASE'):
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }
    else:
        try:
            symbol = data['sym']
            symbol = symbol[:-4]
            binanceUtil = BinanceUtil(
                apiKey=os.environ.get('BINANCE_API_KEY'),
                secretKey=os.environ.get('BINANCE_SECRET_KEY'),
                testnet=os.environ.get('TESTNET'),
            )
            openedTrades = binanceUtil.get_list_trades()
            if len(openedTrades) < binanceUtil.concurrentTrades:
                symbolTrade = [trade for trade in openedTrades if trade['symbol'] == symbol]
                if not symbolTrade:
                    if data['type'] == 'Buy':
                        binanceUtil.openLong(
                            symbol=symbol,
                            leverage=10,
                            stopLossPrice=data['SL'],
                            takeProfitPrice=data['TP']
                        )
                    else:
                        binanceUtil.openShort(
                            symbol=symbol,
                            leverage=10,
                            stopLossPrice=data['SL'],
                            takeProfitPrice=data['TP']
                        )
                else:
                    return f'Trade para {symbol} já aberto'
            else:
                return f'Quantidade maxima de trades ja em andamento'
        except:
            traceback.print_exc()
            abort(500)
    return "OK"