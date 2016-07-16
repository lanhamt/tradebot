#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import time
import json
import threading
import utils
import random


flowLock = threading.Lock()
order_id = 0


class Order:
    def __init__(self, Type='', Order_Id=0, Symbol='', Dir='', Price='', Size=''):
        global order_id
        Order_Id = order_id
        order_id += 1
        self.Type = Type
        self.Order_Id = Order_Id
        self.Symbol = Symbol
        self.Dir = Dir
        self.Price = Price
        self.Size = Size

    def getOrderString(self):
        return json.dumps("{'type': '%s', 'order_id': %s, 'symbol': '%s', 'dir': '%s', 'price': %s, 'size': %s}" % (self.Type, self.Order_Id, self.Symbol, self.Dir, self.Price, self.Size))


def bondTrader(exchange):
    global flowLock
    print('  bond trader is starting')
    while True:
        print('hello')
        time.sleep(1)


def bondBuyExec(prices):
    price = prices.getStockSell('BOND')
    if price[0] < 1000:
        order = Order('add', 0, 'BOND', 'BUY', price[0], price[1])
        print(order.getOrderString(), file=prices.exchange)
        print(order.getOrderString())


def bondBuyCond(prices):
    if prices.getStockSell('BOND')[0] < 1000:
        return True
    return False


def bondSell(prices):
    pass


def bondSellCond(prices):
    pass


def registerAlgos(prices):
    prices.registerEvent(utils.Event(['BOND'], bondBuyCond, bondBuyExec))
    prices.registerEvent(utils.Event(['BOND'], bondSellCond, bondSellExec))


def sayHello(exchange):
    hello = {'type': 'hello', 'team': 'SEGFAULT'}
    print(json.dumps(hello), file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print('The exchange replied:', hello_from_exchange, file=sys.stderr)
    return hello_from_exchange


def trade(exchange):
    global flowLock
    sayHello(exchange)

    prices = utils.Prices(exchange)
    registerAlgos(prices)

    id_no = 0
    # threading.Thread(target=bondTrader, args=(exchange, ))
    while True:
        response = exchange.readline().strip()
        response = json.loads(response)
        utils.processMsg(response, prices)
        if response['type'] != 'book' and response['type'] != 'trade':
            print(response)


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('production', 25000))
    return s.makefile('w+', 1)


def main():
    print('starting tradebot...')
    connected = False
    try:
        exchange = connect()
        connected = True
    except:
        print('  could not connect, retrying')
        connected = False
    if connected:
        trade(exchange)


if __name__ == '__main__':
    main()
