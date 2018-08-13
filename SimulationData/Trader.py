from datetime import *
import pandas as pd


# RawSignals:  = {"DateTime":[], "TargetPosition":[], "MarketPrice":[], "Ticker":[]}
# 不同Ticker在字典列表中区分
# 方便直接传入 pd.DataFrame
class Trader:
	def __init__(self, trader_name, strategy_name):
		self.name = trader_name
		self.owner_strategy = strategy_name
		self.start_date = ""
		self.end_date = ""
		self.RawSignals = {"DateTime":[], "TargetPosition":[], "MarketPrice":[], "Ticker":[]}
		self.Pnls = []

	def add_raw_signals(self, data):
		self.RawSignals['DateTime'].append(data['DateTime'])
		self.RawSignals['TargetPosition'].append(data['TargetPosition'])
		self.RawSignals['MarketPrice'].append(data['MarketPrice'])
		self.RawSignals['Ticker'].append(data['Ticker'])

	# def gen_market_price(self):
	# 	list_ticker = list(set(self.RawSignals["Ticker"]))
	# 	df = pd.DataFrame()
	# 	if len(list_ticker) == 1:
	# 		df = pd.DataFrame(
	# 			index=self.RawSignals["DateTime"],
	# 			data={
	# 				"MarketPrice":self.RawSignals["MarketPrice"],
	# 				"Ticker":self.RawSignals["Ticker"]}
	# 		)
	# 	elif len(list_ticker) == 2:
	# 		df = pd.DataFrame(self.RawSignals)[["DateTime", "MarketPrice", "Ticker"]]
	# 		df = df.pivot(index="DateTime", columns="Ticker", values="MarketPrice")
	# 		df['MarketPrice'] = df[list_ticker[0]] / df[list_ticker[1]]
	# 		df = df["MarketPrice"]
	# 		df['Ticker'] = "%s / %s" %(list_ticker[0], list_ticker[1])
	# 	return df

	def add_pnls(self, data):
		self.Pnls.append(data)
