import utils
def XLFtoStockTest(prices):
	XLFTuple = prices.getStockBuy("XLF")
	BondTuple = prices.getStockSell("BOND")
	GSTuple = prices.getStockSell("GS")
	MSTuple = prices.getStockSell("MS")
	WFCTuple prices.getStockSell("WFC")

	max_trade = min(XLFTuple[1]/10, BondTuple[1]/3, GSTuple[1]/2, MSTuple[1]/3, WFCTuple[1]/2)
	XLFValue = XLFTuple[0]*max_trade*10
	BundleValue = sum(BondTuple[0]*max_trade*3, GSTuple[0]*max_trade*2, MSTuple[0]*max_trade*3, WFCTuple[0]*max_trade*2)
	if XLFValue + 100 < BundleValue:
		tradeXLF(max_trade)

def tradeXLF(trade_sz):
	utils.buy("XLF", trade_sz*10)
	utils.convert("XLF", False, trade_sz*10) #True = BUY
	utils.sell("BOND", trade_sz*3)
	utils.sell("GS", trade_sz*2)
	utils.sell("MS", trade_sz*3)
	utils.sell("WFC", trade_sz*2)

def XLFtoStockTest(prices):
	XLFTuple = prices.getStockSell("XLF")
	BondTuple = prices.getStockBuy("BOND")
	GSTuple = prices.getStockBuy("GS")
	MSTuple = prices.getStockBuy("MS")
	WFCTuple prices.getStockBuy("WFC")

	max_trade = min(XLFTuple[1]/10, BondTuple[1]/3, GSTuple[1]/2, MSTuple[1]/3, WFCTuple[1]/2)
	XLFValue = XLFTuple[0]*max_trade*10
	BundleValue = sum(BondTuple[0]*max_trade*3, GSTuple[0]*max_trade*2, MSTuple[0]*max_trade*3, WFCTuple[0]*max_trade*2)
	if BundleValue + 100 < XLFValue:
		tradeXLFBundle(max_trade)



def tradeXLFBundle(trade_sz):
	utils.buy("BOND", trade_sz*3)
	utils.buy("GS", trade_sz*2)
	utils.buy("MS", trade_sz*3)
	utils.buy("WFC", trade_sz*2)
	utils.convert("XLF", True, trade_sz*10) #True = BUY
	utils.sell("XLF", trade_sz*10)

	