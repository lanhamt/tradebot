#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import random
import time

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("production", 20000))
    return s.makefile('w+', 1)

def main():
    exchange = connect()
    print("HELLO SEGFAULT", file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print('The exchange replied:', hello_from_exchange, file=sys.stderr)
    id_no = 0
    while True:
#    	print('ADD ' + str(id_no) + ' BOND BUY 999 10', file=exchange)
#        print('ADD ' + str(id_no) + ' BOND SELL 1001 1', file=exchange)
    	id_no += 1
        time.sleep(.08)
        response = exchange.readline().strip()
    	print(response)

if __name__ == '__main__':
    main()
