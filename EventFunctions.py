import utils

"""
Determines if buying XLF, converting it to the bundle and reselling the bundle is a good idea and executes
Should be attacked to: ["XLF","BOND","GS","MS","WFC"]
"""
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


"""
Determines if buying the XLF components, converting it to an XLF ETF and reselling the ETF is a good idea and executes
Should be attacked to: ["XLF","BOND","GS","MS","WFC"]
"""
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


"""
Checks for a possible transaction between VALE and VALBZ and executes it
"""
def tradeVALEAndVALBZ(prices):
	VALEBuyTuple = prices.getStockSell("VALE")
	VALESellTuple = prices.getStockBuy("VALE")
	VALBZBuyTuple = prices.getStockSell("VALBZ")
	VALBZSellTuple = prices.getStockSell("VALBZ")
	max_tradeVALE2VALBZ = min(VALEBuyTuple[1], VALBZSellTuple[1])
	max_tradeVALBZ2VALE = min(VALBZBuyTuple[1], VALESellTuple[1])
	if VALEBuyTuple[0]*max_tradeVALE2VALBZ + 10 < VALBZSellTuple[0]*max_tradeVALE2VALBZ:
		tradeVALEforVALBZ(max_tradeVALE2VALBZ)
	if VALBZBuyTuple[0]*max_tradeVALBZ2VALE + 10 < VALESellTuple[0]*max_tradeVALBZ2VALE:
		tradeVALBZforVALE(max_tradeVALBZ2VALE)

def tradeVALEforVALBZ(trade_sz):
	utils.buy("VALE", trade_sz)
	utils.convert("VALE", False, trade_sz)
	utils.sell("VALBZ", trade_sz)

def tradeVALBZforVALE(trade_sz):
	utils.buy("VALBZ", trade_sz)
	utils.convert("VALBZ", False, trade_sz)
	utils.sell("VALE", trade_sz)