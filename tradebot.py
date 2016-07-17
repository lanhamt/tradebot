#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import time
import json
import thread
import utils
import random
from utils import Order


def buy(prices, name, size, price):
    order = Order('add', 0, name, 'BUY', price, size)
    print(order.getOrderString(), file=prices.exchange)
    print('ORDER SUBMITTED [BUY]: ', order.getOrderString())


def sell(prices, name, size, price):
    order = Order('add', 0, name, 'SELL', price, size)
    print(order.getOrderString(), file=prices.exchange)
    print('ORDER SUBMITTED [SELL]', order.getOrderString())


def convert(prices, name, is_buy, size):
    order = Order('convert', 0, name, 'BUY', Size=size)


def bondBuyExec(prices):
    price = prices.getStockSell('BOND')
    if price[0] < 1000:
        order = Order('add', 0, 'BOND', 'BUY', price[0], price[1])
        print(order.getOrderString(), file=prices.exchange)
        print(order.getOrderString())


def bondBuyCond(prices):
    return True


def bondSellExec(prices):
    price = prices.getStockBuy('BOND')
    if price[0] > 1000:
        order = Order('add', 0, 'BOND', 'SELL', price[0], price[1])
        print(order.getOrderString(), file=prices.exchange)
        print(order.getOrderString())


def bondSellCond(prices):
    return True


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
    thread.start_new_thread(status, (exchange, ))
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
