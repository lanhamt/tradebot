import sys
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
		self.checkEvents(self.stocks[name])
	def setStockBuy(self, name, buyPrice):
		if name in self.stocks:
			self.stocks[name].buyPrice = buyPrice
		else :
			self.stocks[name] = Stock(name, buyPrice=buyPrice)
		self.checkEvents(self.stocks[name])
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
	def checkEvents(self, stock):
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
	bestBuyPrice = sorted(buyPrices, key=lambda price: price[0])[len(buyPrices) - 1]
	bestSellPrice = sorted(sellPrices, key=lambda price: price[0])[0]
	prices.setStockBuy(name, bestBuyPrice)
	prices.setStockSell(name, bestSellPrice)

def processMsg(msg, prices):
	if msg['type'] == 'book':
		processBookJSON(msg, prices)
