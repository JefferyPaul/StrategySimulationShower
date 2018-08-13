from datetime import *
import pandas as pd


# PureObject
class RawSignal:
	def __init__(self, data):
		self.datetime = data[0]
		self.targetPosition = float(data[1])
		self.mkp = float(data[2])


# 输入整份RawSignals.csv文件数据——DataFrame格式，整理
	# def __init__(self, strategy, trader, file_data):
	# 	self.Strategy = strategy
	# 	self.Trader = trader
	#
	# 	self.Tickers = list(file_data['Ticker'].unique())
	# 	self.ticker_data = {}
	# 	for i_ticker in self.Tickers:
	# 		self.ticker_data[i_ticker] = pd.DataFrame(file_data[file_data['Ticker'] == i_ticker])
	#
	# 	self.start_date = min(list(file_data['Date'].unique()))
	# 	self.end_date = max(list(file_data['Date'].unique()))
	# 	self.InitX = int(list(file_data['InitX'].unique())[0])
	#
	# 	# One Ticker or Two Ticker
	# 	# 1 Position
	# 	self.TargetPosition = {}
	# 	self.StdTargetPosition = {}
	# 	for i_ticker in self.Tickers:
	# 		self.TargetPosition[i_ticker] = self.ticker_data[i_ticker].loc[:, ['Date', 'Time', 'TargetPosition']]
	# 		self.StdTargetPosition[i_ticker] = pd.concat([self.TargetPosition[i_ticker].loc[:, ['Date', 'Time']],
	# 		                                              round(self.TargetPosition[i_ticker].loc[:, 'TargetPosition'] /
	# 			                                              max(abs(self.TargetPosition[i_ticker].loc[:, 'TargetPosition'])), 2)
	# 		                                              ], axis=1)
	# 	# 2 MkP
	# 	if len(self.Tickers) == 1:
	# 		self.MkP = self.ticker_data[self.Tickers[0]].loc[:, ['Date', 'Time', 'Close']]
	# 	elif len(self.Tickers) == 2:
	# 		mkp1 = self.ticker_data[self.Tickers[0]].loc[:,['Close']]
	# 		mkp2 = self.ticker_data[self.Tickers[1]].loc[:, ['Close']]
	# 		mkp = pd.Series(data = mkp1/mkp2, name = "MkP")
	# 		self.MkP = pd.concat([self.ticker_data[self.Tickers[0]].loc[:,['Date', 'Time']], mkp], axis=1)
	# 	else:
	# 		pass
	#
	# 	# 清空
	# 	file_data, mkp1, mkp2, mkp = [""] * 4
