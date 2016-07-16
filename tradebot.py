#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import random
import time
import json
import threading
import utils


flowLock = threading.Lock()


def bondTrader(exchange):
    global flowLock
    print('  bond trader is starting')
    while True:
        pass


def bondBuyExec(prices):
    price = prices.getStockSell('BOND')
    if price[0] < 1000:
        buy_order = {'type': 'trade', 'symbol': 'BOND', 'price': price[0], 'size': price[1]}
        print(json.dumps(buy_order), file=prices.exchange)


def bondBuyCond(prices):
    if prices.getStockSell('BOND')][0] < 1000:
        return True
    return False


def registerAlgos(prices):
    prices.registerEvent(['BOND'], bondBuyCond, )


def sayHello(exchange):
    hello = {'type': 'hello', 'team': 'SEGFAULT'}
    print(json.dumps(hello), file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print('The exchange replied:', hello_from_exchange, file=sys.stderr)


def trade(exchange):
    global flowLock
    sayHello(exchange)

    prices = utils.Prices(exchange)
    registerAlgos(prices)

    id_no = 0
    threading.Thread(target=bondTrader, args=(exchange, ))
    while True:
        flowLock.acquire()
        response = exchange.readline().strip()
        flowLock.release()
        response = json.loads(response)
        utils.processMsg(response, prices)
        if response['type'] != 'book' and response['type'] != 'trade':
            print(response)
#        print('ADD ' + str(id_no) + ' BOND BUY 999 10', file=exchange)
#        print('ADD ' + str(id_no) + ' BOND SELL 1001 1', file=exchange)
#        id_no += 1
#        time.sleep(.08)


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('production', 25000))
    return s.makefile('w+', 1)


def main():
    print('starting tradebot...')
    try:
        exchange = connect()
        trade(exchange)
    except:
        print('  could not connect, retrying')


if __name__ == '__main__':
    main()
