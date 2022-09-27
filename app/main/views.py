from . import main
import traceback
import json, os
from flask import request, abort
from dotenv import load_dotenv
from ..binance_functions import BinanceUtil

load_dotenv()

@main.route('/')
def index():
    return 'Trading Bot1 - teste'

@main.route('/env',methods=['POST','GET'])
def env():
    return 'BINANCE_API_KEY: ' + os.getenv('BINANCE_API_KEY')

@main.route('/testeBinance', methods=['POST','GET'])
def testeBinance():
    testnet = os.environ.get('TESTNET') == 'True'
    binanceUtil = BinanceUtil(
        apiKey=os.environ.get('BINANCE_API_KEY'),
        secretKey=os.environ.get('BINANCE_SECRET_KEY'),
        testnet=testnet,
        percentualSizeTrade=float(os.environ.get('PERCENTUAL_SIZE_TRADE')),
        leverage=int(os.environ.get('LEVERAGE')),
        concurrentTrades=int(os.environ.get('CONCURRENT_TRADES')),
        useTrailing= os.environ.get('USE_TRAILING') == 'True',
        callBackRate= float(os.environ.get('CALLBACK_RATE')),
        activationPerc=float(os.environ.get('ACTIVATION_PERC'))
    )
    return str(binanceUtil.get_account_balance('USDT'))


@main.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    if data['pwd'] != os.environ.get('WEBHOOK_PASSPHRASE'):
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }
    else:
        try:
            if os.getenv('BOT_ATIVO') != 'True':
                return 'Bot Inativo'
            symbol = data['sym']
            symbol = symbol[:-4]
            testnet = os.environ.get('TESTNET') == 'True'
            binanceUtil = BinanceUtil(
                apiKey=os.environ.get('BINANCE_API_KEY'),
                secretKey=os.environ.get('BINANCE_SECRET_KEY'),
                testnet=testnet,
                percentualSizeTrade=float(os.environ.get('PERCENTUAL_SIZE_TRADE')),
                leverage=int(os.environ.get('LEVERAGE')),
                concurrentTrades=int(os.environ.get('CONCURRENT_TRADES')),
                useTrailing=os.environ.get('USE_TRAILING') == 'True',
                callBackRate=float(os.environ.get('CALLBACK_RATE')),
                activationPerc=float(os.environ.get('ACTIVATION_PERC'))
            )
            openedTrades = binanceUtil.get_list_trades()
            if len(openedTrades) < binanceUtil.concurrentTrades:
                symbolTrade = [trade for trade in openedTrades if trade['symbol'] == symbol]
                if not symbolTrade:
                    if data['type'] == 'Buy':
                        binanceUtil.openLong(
                            symbol=symbol,
                            stopLossPrice=data['SL'],
                            takeProfitPrice=data['TP']
                        )
                    else:
                        binanceUtil.openShort(
                            symbol=symbol,
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