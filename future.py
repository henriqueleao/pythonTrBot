# https://algotrading101.com/learn/binance-python-api-guide/
# https://github.com/sammchardy/python-binance

# https://academy.binance.com/pt/articles/understanding-the-different-order-types
# https://blog.quantinsti.com/crypto-arbitrage/
# https://www.ig.com/en/trading-strategies/how-to-hedge-bitcoin-risk-190726

# https://www.youtube.com/watch?v=nWzNYh0ccqI

# chaves de testes - FUTURE
api_secret = '8804cc512c355aba5f67839de0ebddd307d0c5ffece7b00bae384385df44a3be'
api_key = '8e62eaa28bb4edf56064a9606372496eca4b13307f02feab609fb971467a0c3b'

from binance import Client
# from time import sleep
# from binance import ThreadedWebsocketManager

# o parâmetro testnet utiliza o Spot test network, permitindo que sejam feitos testes, sem impactar a conta
client = Client(api_key, api_secret, testnet=True)
# Spot testnet base url: https://testnet.binance.vision
# Spot production base url: https://api.binance.com
# Futures Testnet base url: https://testnet.binancefuture.com
# Futures production base url: https://fapi.binance.com
# Delivery futures testnet base url: https://testnet.binancefuture.com
# Delivery futures production base url: https://dapi.binance.com

client.API_URL = 'https://testnet.binancefuture.com'

# get latest price from Binance API
# btc_price = client.futures_symbol_ticker(symbol="BTCUSDT")

# print full output (dictionary)
# print(btc_price)

def saldo_atual():
    """
    imprime todos os ativos da carteira e seus repectivos valores
    """
    for asset in client.futures_account_balance():
        print(f"{asset['asset']}: {asset['balance']}")

def saldo_crypto(moeda):
    """
    moeda indica o símbolo da moeda a ser buscado o saldo
    Retorna o saldo da moeda indicada na carteira
    """
    resultado = next((ativo for ativo in client.futures_account_balance() if ativo["asset"] == moeda), None)
    valor = 0
    if resultado != None:
        valor = resultado['balance']
    return valor

def moeda_precisao(moeda):
    for x in client.futures_exchange_info()['symbols']:
        if x['symbol'] == moeda:
            return x['pricePrecision']

def compra_crypto(moeda, tipo, quantidade, alavancagem):
    """
    moeda é o símbolo da moeda que será comprada (ex: BTCUSDT)
    tipo indica o tipo de compra (MARKET - compra ou venda imediata | LIMIT - espera o preço atingir um valor para comprar ou vender)
    quantidade indica a quantidade em USDT a ser utilizado para comprar a moeda desejada
    alavancagem é o multiplicador utilizado na operação
    """
    # seta a alanvancagem da crypto a ser comprada
    client.futures_change_leverage(symbol=moeda, leverage=alavancagem)

    # pega o preço atual da moeda desejada
    preco_atual = float(client.futures_symbol_ticker(symbol=moeda)['price'])

    # seta o tipo de margem para isolado
    #client.futures_change_margin_type(symbol='BTCUSDT', marginType='ISOLATED')
    precisao = moeda_precisao(moeda)

    # https://binance-docs.github.io/apidocs/futures/en/#new-order-trade
    ordens = []
    ordens.append(client.futures_create_order(
        symbol=moeda,
        side='BUY',
        type=tipo,
        quantity=round(quantidade/preco_atual, 2)
    ))

    ordens.append(client.futures_create_order(
        symbol=moeda,
        side='SELL',
        type='STOP_MARKET',
        stopPrice=round(preco_atual * 0.98, precisao), # seta o stopPrice para o valor atual da moeda
        closePosition='true'
    ))

    return ordens

def vende_crypto(moeda):
    """
    moeda é o símbolo da moeda que será vendida (ex: BTCUSDT)
    retorna os dados da venda da criptomoeda indicada
    """
    ordens = []
    ordens.append(client.futures_create_order(
        symbol=moeda,
        side='SELL',
        type='MARKET',
        quantity=100,
        reduceOnly='true'
    ))

    return ordens

def retorna_orders(status):
    """
    status string que indica o status dos pedidos (NEW - open order, EXPIRED - , FILLED - finalizados, CANCELED - pedidos deletados)
    retorna uma lista com os pedidos contendo o status indicado
    """
    retorno = []
    for order in client.futures_get_all_orders():
        if order['status'] == status:
            retorno.append(order)
    
    return retorno

def quantidade_moeda_posicao(moeda):
    """
    moeda é o símbolo da moeda (ex: BTCUSDT)
    retorna a quantidade da moeda indicada para a posição
    """
    lista = []
    for order in retorna_orders('FILLED'):
        if order['symbol'] == moeda and order['side'] == 'BUY':
            lista.append(order)
            #return order['origQty']
    return lista

# saldo_atual()
# print(saldo_crypto('USDT'))
# print(compra_crypto('LTCUSDT','MARKET', 60, 1))
#print(vende_crypto('LTCUSDT'))

#print(quantidade_moeda_posicao('LTCUSDT'))

# {'orderId': 3196363807, 'symbol': 'BTCUSDT', 'status': 'NEW', 'clientOrderId': 'FIa5N8z345xyKFDgaWCwxl', 'price': '0', 'avgPrice': '0.00000', 'origQty': '0.001', 'executedQty': '0', 'cumQty': '0', 'cumQuote': '0', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'updateTime': 1660571071396}

#print(retorna_orders('CANCELED'))

# print(client.futures_symbol_ticker(symbol='ETHUSDT')['price'])

# print(moeda_precisao('LTCUSDT'))

# get balances for margin account
# print(client.get_margin_account())