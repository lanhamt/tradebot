#!/usr/bin/python
from __future__ import print_function
import sys
import socket
import time
import json
import thread
import m3_utils
import random
from m3_utils import Order
from m3_event_functions import *


lines = 0


def portfolioStats(prices):
	global lines
	while True:
		print('PORTFOLIO STATS:\n')
		print(prices.portfolio.printStats() + '\n')
		print('COMM LINES: ' + str(lines) + '\n')
		time.sleep(10)


def registerAlgos(prices):
    prices.registerEvent(m3_utils.Event(['BOND'], dummy, bondBuyExec))
    prices.registerEvent(m3_utils.Event(['BOND'], dummy, bondSellExec))
    prices.registerEvent(m3_utils.Event(["XLF","BOND","GS","MS","WFC"], dummy, XLFtoStockTest))
    prices.registerEvent(m3_utils.Event(["XLF","BOND","GS","MS","WFC"], dummy, StocktoXFLTest))
    prices.registerEvent(m3_utils.Event(['VALE', 'VALBZ'], dummy, tradeVALEAndVALBZ))
    prices.registerEvent(m3_utils.Event(['BOND','VALBZ','VALE','GS','MS','WFC','XLF'], dummy, liquidate))


def sayHello(exchange):
    hello = {'type': 'hello', 'team': 'SEGFAULT'}
    print(json.dumps(hello), file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print('The exchange replied:', hello_from_exchange, file=sys.stderr)
    return json.loads(hello_from_exchange)


def trade(exchange):
    global lines
    initial_balance = sayHello(exchange)

    prices = m3_utils.Prices(exchange, initial_balance)
    registerAlgos(prices)

    thread.start_new_thread(portfolioStats, (prices,))
    while True:
        response = exchange.readline().strip()
        response = json.loads(response)
        m3_utils.processMsg(response, prices)
        lines += 1


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('test-exch-segfault', 25000))
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
