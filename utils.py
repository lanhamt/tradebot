class stock:
	name = ""
	ETF = False
	members = []
	sellPrice = 0
	buyPrice = 0
	def __init__(self, name, ETF = False, members = [], sellPrice = 0, buyPrice = 0)

class Prices:
	stocks = {}
	def setStockSell(self, name, sellPrice):
		if name in self.stocks:
			self.stocks[name].sellPrice = sellPrice
		else :
			self.stocks[name] = stock(name, sellPrice=sellPrice)
	def setStockBuy(self, name, buyPrice):
		if name in self.stocks:
			self.stocks[name].buyPrice = buyPrice
		else :
			self.stocks[name] = stock(name, buyPrice=buyPrice)
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


def processBookJSON(msg, prices):
	name = msg.symbol
	buyPrices = msg.buy
	sellPrices = msg.sell
	bestBuyPrice = sorted(buyPrices, key=lambda price: price[0])[len(buyPrices) - 1]
	bestSellPrice = sorted(sellPrices, key=lambda price: price[0])[0]
	prices.setStockBuy(name, bestBuyPrice)
	prices.setStockSell(name, bestSellPrice)


