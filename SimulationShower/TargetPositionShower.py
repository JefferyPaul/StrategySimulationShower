import pandas as pd
from datetime import *
import os
import DataManger
from SimulationData import Parse
from SimulationData.Trader import Trader
from pyecharts import Line, Grid, Page



# 数据文件的 Strategy 、 traders 名字与策略中所用字符 的一致性问题
# TraderFolderName 包含IP Port所以TraderFolderName与TraderName 必须分开，需要处理
# StrategyName的选择与输入可以由程序提供，所以可以完全按照路径名字
# TraderName = TraderFolderName.split("@")[0]

# Ticker与Trader
# 选择用Trader
# 内部pair策略存放数据时用Ticker区分

# 输入所选择 Strategy、traders
# 寻找数据（的路径）
# 输入至RawSignals
# 存放RawSignals
# 显示
class TargetPositionShower:
	def __init__(self, strategies, traders):
		if type(strategies) == list:
			self.chose_strategies = strategies
		else:
			self.chose_strategies = [strategies]
		if type(traders) == list:
			self.chose_traders = traders
		else:
			self.chose_traders = [traders]

		self.TargetPositionData = {}
	# self.TargetPositionData = { "i_strategy_name1": [Trader, Trader ], "i_strategy_name2": [] }
	# Trader (class):  Trader.name,Trader.owner_strategy,Trader.start_date,Trader.end_date,Trader.RawSignals,Trader.Pnls

	# 获取所选择内容的数据

	def get_selected_data(self):
		# 数据以文件、文件夹形式存放
		# 获取所选择strategy、traders 数据所在的目录
		# 返回目标数据所在目录   { "strategyA": { "traderA":traderA_path, "":, }, "":{} }
		dict_data_folder_path = DataManger.get_data_path(self.chose_strategies, self.chose_traders)

		# datas   { "i_strategy_name": [ ], }
		datas = {}
		for i_strategy_name in dict_data_folder_path.keys():
			datas[i_strategy_name] = []
			for i_trader_name in dict_data_folder_path[i_strategy_name].keys():
				i_trader_path = dict_data_folder_path[i_strategy_name][i_trader_name]

				obj_traders = Trader(i_trader_name, i_strategy_name)

				trader_raw_signal_path = os.path.join(i_trader_path, 'RawSignals.csv')
				with open(trader_raw_signal_path, encoding='gb2312') as f:
					while True:
						line_data = f.readline()
						if line_data == "":
							break
						if line_data.find("Date") == -1:
							# 用多个 PureObject装住每一行数据 ？
							# d_raw_signal = RawSignal(Parse.parse_raw_signals_csv(line_data))
							# obj_traders.add_raw_signals(d_raw_signal)
							# 或者,用一个 DataFrame装住多行数据 ？
							obj_traders.add_raw_signals(Parse.parse_raw_signals_csv(line_data))
				datas[i_strategy_name].append(obj_traders)
		self.TargetPositionData = datas

	# 2  根据显示需求，
	# 1： 单ticker 多Strategy

	# 分别对每一个trader拿数据
	# 然后画图
	# 在合并图片
	def show_traders(self, start, end):
		def get_std_target_price(df):
			df = df.set_index("DateTime")
			std_tp = df['TargetPosition'] / max(abs(df['TargetPosition']))
			return std_tp

		def set_date_range():
			pass

		def add_target_price_line(line_obj, df):
			line_obj.add(
				"%s-%s" % (strategy_name, ticker_name),
				x_axis=df.index.tolist(),
				y_axis=[round(i, 2) for i in df.tolist()],
				is_datazoom_show=True,
				datazoom_xaxis_index=[0, 1],
				legend_top="0%"
			)

		def get_pair_market_price(df):
			df_tickers_pivot = df.pivot(index="DateTime", columns="Ticker", values="MarketPrice")
			df_tickers_pivot['MarketPrice'] = \
				df_tickers_pivot[list_ticker_name[0]] / df_tickers_pivot[list_ticker_name[1]]
			df_market_price = df_tickers_pivot[["MarketPrice"]]
			df_market_price["Tickers"] = "%s / %s" % (list_ticker_name[0], list_ticker_name[1])
			return df_market_price

		start_date = datetime.strptime(start, "%Y-%m-%d")
		end_date = datetime.strptime(end, "%Y-%m-%d")

		# 重整self.TargetPosition顺序
		dict_traders = {}
		for strategy_name in self.TargetPositionData.keys():
			for trader_obj in self.TargetPositionData[strategy_name]:
				if trader_obj.name not in dict_traders.keys():
					dict_traders[trader_obj.name] = []
				dict_traders[trader_obj.name].append(trader_obj)

		# 取数据并画图
		dict_TargetP_line = {}
		dict_MKP_line = {}
		dict_Grid = {}
		for trader_name in dict_traders.keys():
			dict_TargetP_line[trader_name] = Line()
			dict_MKP_line[trader_name] = Line()
			dict_Grid[trader_name] = Grid()

			df_market_price_longer = pd.DataFrame()
			for trader_obj in dict_traders[trader_name]:
				strategy_name = trader_obj.owner_strategy

				# 日期处理
				df_trader_raw_signals = pd.DataFrame(trader_obj.RawSignals)
				if len(start) > 0:
					df_trader_raw_signals = df_trader_raw_signals[df_trader_raw_signals['DateTime'] > start_date]
				if len(end) > 0:
					df_trader_raw_signals = df_trader_raw_signals[df_trader_raw_signals['DateTime'] < end_date]

				list_ticker_name = list(df_trader_raw_signals['Ticker'].unique())

				for ticker_name in list_ticker_name:
					df_ticker_raw_signals = df_trader_raw_signals[df_trader_raw_signals['Ticker'] == ticker_name]
					df_std_target_price = get_std_target_price(df_ticker_raw_signals)
					add_target_price_line(
						dict_TargetP_line[trader_name],
						df_std_target_price)

				if len(list_ticker_name) == 1:
					df_market_price = df_trader_raw_signals[['MarketPrice','Ticker']]
				else:
					try:
						df_market_price = get_pair_market_price(df_trader_raw_signals)
					except:
						print(" Wrong in get_pair_market_price")
						df_market_price = pd.DataFrame()

				if len(df_market_price) > len(df_market_price_longer):
					df_market_price_longer = df_market_price

			dict_MKP_line[trader_name].add(
				"%s" % list(df_market_price_longer["Tickers"].unique())[0],
				x_axis=df_market_price_longer.index.tolist(),
				y_axis=df_market_price_longer['MarketPrice'].tolist(),
				yaxis_max=round(max(df_market_price_longer['MarketPrice'].tolist()), 2) + 0.01,
				yaxis_min=round(min(df_market_price_longer['MarketPrice'].tolist()), 2) - 0.01,
				yaxis_pos="right",
				is_datazoom_show=True,
				legend_top="10%"
			)

			dict_Grid[trader_name].add(
				dict_TargetP_line[trader_name],
				grid_top="20%"
			)
			dict_Grid[trader_name].add(
				dict_MKP_line[trader_name],
				grid_top="20%"
			)

		page = Page()
		for grid_key in dict_Grid:
			page.add(dict_Grid[grid_key])
		page.render(r"./output/%s-%s.html" % (self.chose_strategies[0], self.chose_traders[0]))

	# 2： 单strategy 多Strategy
