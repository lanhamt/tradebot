#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import random
import time
import json


def sayHello(exchange):
    hello = {"type": "hello", "team": "SEGFAULT"}
    print(json.dumps(hello), file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print('The exchange replied:', hello_from_exchange, file=sys.stderr)


def trade(exchange):
    sayHello(exchange)
    id_no = 0
    while True:
        response = exchange.readline().strip()
        response = json.loads(response)
        if response['type'] is not 'book':
            print(response)
#        print('ADD ' + str(id_no) + ' BOND BUY 999 10', file=exchange)
#        print('ADD ' + str(id_no) + ' BOND SELL 1001 1', file=exchange)
#        id_no += 1
#        time.sleep(.08)


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("production", 25000))
    return s.makefile('w+', 1)


def main():
    print("starting tradebot...")
    try:
        exchange = connect()
        trade(exchange)
    except:
        print("  could not connect, retrying")


if __name__ == '__main__':
    main()
