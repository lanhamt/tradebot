class Stock:
	name = ''
	ETF = False
	members = []
	sellPrice = 0
	buyPrice = 0
	def __init__(self, name, ETF = False, members = [], sellPrice = (float('inf'), 0), buyPrice = (0, 0))

class Event:
	triggerStocks = []
	testFunc = None 
	actionFunc = None
	def __init__(self, triggerStocks, testFunc, actionFunc):
		self.triggerStocks = triggerStocks
		self.testFunc = testFunc
		self.actionFunc = actionFunc

class Prices:
	stocks = {}
	stockEvents = {}
	exchange = None
	def setStockSell(self, name, sellPrice):
		if name in self.stocks:
			self.stocks[name].sellPrice = sellPrice
		else :
			self.stocks[name] = Stock(name, sellPrice=sellPrice)
		self.checkEvents(stocks[name])
	def setStockBuy(self, name, buyPrice):
		if name in self.stocks:
			self.stocks[name].buyPrice = buyPrice
		else :
			self.stocks[name] = Stock(name, buyPrice=buyPrice)
		self.checkEvents(stocks[name])
	def addNewStock(stock):
		self.stocks[stock.name] = stock
	def getStockSell(name):
		return self.stocks[name].sellPrice
	def getStockBuy(name):
		return self.stocks[name].buyPrice
	def isETF(name):
		return self.stocks[name].ETF
	def getMembers(name):
		return self.stocks[name].members
	def registerEvent(self, event):
		for stockName in event.triggerStocks:
			if stockName in self.stockEvents:
				self.stockEvents[stockName].append(event)
			else :
				self.stockEvents[stockName] = [event]
	def checkEvents(stock)
		if stock.name in self.stockEvents:
			for event in self.stockEvents[stock.name]:
				if event.testFunc(self):
					event.actionFunc(self)
	def __init__(self, exchange):
		self.exchange = exchange
		self.stocks['BOND'] = stock('BOND')
		self.stocks['VALBZ'] = stock('VALBZ', True, [('VALE', 1)])
		self.stocks['VALE'] = stock('VALE', True, [('VALBZ', 1)])
		self.stocks['GS'] = stock('GS')
		self.stocks['MS'] = stock('MS')
		self.stocks['WFC'] = stock('WFC')
		self.stocks['XLF'] = stock('XLF', True, [('BOND', 3), ('GS', 2), ('MS', 3), ('WFC', 2)])


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

def testFunc(prices):
	return True

def buyBonds(prices):
	print('BUYING', file=prices.exchange)

def registerStockEvents(prices):
	prices.registerEvent(['BOND'], testFunc, buyBonds)


def demo():
	prices = Prices()
	registerStockEvents(prices)
	while True:
		msg = getServerMsg()
		processMsg(msg)

'''
Get server message
updateDB
check if action is available
take action
'''