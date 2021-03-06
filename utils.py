import sys
import json

# global var to keep track of last order id
order_id = 0


class Order:
    def __init__(self, Type=None, Order_Id=None, Symbol=None, Dir=None, Price=None, Size=None):
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
        ret = {}
        if self.Type: ret['type'] = self.Type
        if self.Order_Id: ret['order_id'] = self.Order_Id
        if self.Symbol: ret['symbol'] = self.Symbol
        if self.Dir: ret['dir'] = self.Dir
        if self.Price: ret['price'] = self.Price
        if self.Size: ret['size'] = self.Size
        return json.dumps(ret)


class Stock:
    def __init__(self, name, ETF=False, members=[], sellPrice=(float('inf'), 0), buyPrice=(0, 0)):
        self.name = name
        self.ETF = ETF
        self.members = members
        self.sellPrice = sellPrice
        self.buyPrice = buyPrice

class Event:
    def __init__(self, triggerStocks, testFunc, actionFunc):
        self.triggerStocks = triggerStocks
        self.testFunc = testFunc
        self.actionFunc = actionFunc

class Prices:
    def setStockSell(self, name, sellPrice):
        if name in self.stocks:
            self.stocks[name].sellPrice = sellPrice
        else :
            self.stocks[name] = Stock(name, sellPrice=sellPrice)
    def setStockBuy(self, name, buyPrice):
        if name in self.stocks:
            self.stocks[name].buyPrice = buyPrice
        else :
            self.stocks[name] = Stock(name, buyPrice=buyPrice)
    def addNewStock(self, stock):
        self.stocks[stock.name] = stock
    def getStockSell(self, name):
        return self.stocks[name].sellPrice
    def getStockBuy(self, name):
        return self.stocks[name].buyPrice
    def isETF(self, name):
        return self.stocks[name].ETF
    def getMembers(self, name):
        return self.stocks[name].members
    def registerEvent(self, event):
        for stockName in event.triggerStocks:
            if stockName in self.stockEvents:
                self.stockEvents[stockName].append(event)
            else :
                self.stockEvents[stockName] = [event]
    def checkEvents(self, name):
        stock = self.stocks[name]
        if stock.name in self.stockEvents:
            for event in self.stockEvents[stock.name]:
                if event.testFunc(self):
                    event.actionFunc(self)
    def __init__(self, exchange):
        self.stocks = {}
        self.stockEvents = {}
        self.exchange = exchange
        self.stocks['BOND'] = Stock('BOND')
        self.stocks['VALBZ'] = Stock('VALBZ', True, [('VALE', 1)])
        self.stocks['VALE'] = Stock('VALE', True, [('VALBZ', 1)])
        self.stocks['GS'] = Stock('GS')
        self.stocks['MS'] = Stock('MS')
        self.stocks['WFC'] = Stock('WFC')
        self.stocks['XLF'] = Stock('XLF', True, [('BOND', 3), ('GS', 2), ('MS', 3), ('WFC', 2)])


def processBookJSON(msg, prices):
    name = msg['symbol']
    buyPrices = msg['buy']
    sellPrices = msg['sell']
    if (len(buyPrices) > 0):
        bestBuyPrice = sorted(buyPrices, key=lambda price: price[0])[len(buyPrices) - 1]
        prices.setStockBuy(name, bestBuyPrice)
    if(len(sellPrices) > 0):
        bestSellPrice = sorted(sellPrices, key=lambda price: price[0])[0]
        prices.setStockSell(name, bestSellPrice)
    prices.checkEvents(name)

def processMsg(msg, prices):
    if msg['type'] == 'book':
        processBookJSON(msg, prices)
