#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import time
import json
import thread
import exp_utils
import random
from exp_utils import Order
from EventFunctions import *


def registerAlgos(prices):
    prices.registerEvent(exp_utils.Event(['BOND'], dummy, bondBuyExec))
    prices.registerEvent(exp_utils.Event(['BOND'], dummy, bondSellExec))
    prices.registerEvent(exp_utils.Event(["XLF","BOND","GS","MS","WFC"], dummy, XLFtoStockTest))
    prices.registerEvent(exp_utils.Event(["XLF","BOND","GS","MS","WFC"], dummy, StocktoXFLTest))
    prices.registerEvent(exp_utils.Event(['VALE', 'VALBZ'], dummy, tradeVALEAndVALBZ))


def sayHello(exchange):
    hello = {'type': 'hello', 'team': 'SEGFAULT'}
    print(json.dumps(hello), file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print('The exchange replied:', hello_from_exchange, file=sys.stderr)
    return hello_from_exchange


def trade(exchange):
    global flowLock
    sayHello(exchange)

    prices = exp_utils.Prices(exchange)
    registerAlgos(prices)

    id_no = 0
    thread.start_new_thread(status, (exchange, ))
    while True:
        response = exchange.readline().strip()
        response = json.loads(response)
        exp_utils.processMsg(response, prices)
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
