#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import time
import json
import threading
import utils


flowLock = threading.Lock()


class Order:
    def __init__(self, Type='', Symbol='', Price='', Size=''):
        self.Type = Type
        self.Symbol = Symbol
        self.Price = Price
        self.Size = Size

    def getOrderString(self):
        return json.dumps("{'type': '%s', 'symbol', '%s', 'price': '%s', 'size': '%s'}" % (self.Type, self.Symbol, self.Price, self.Size))


class Book:
    def __init__(self):
        self.stocks = []
        self.price = 0


def bondTrader(exchange):
    global flowLock
    print('  bond trader is starting')
    while True:
        hello_resp = sayHello(exchange)


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
    threading.Thread(target=bondTrader, args=(exchange, ))
    while True:
        flowLock.acquire()
        response = exchange.readline().strip()
        flowLock.release()
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
