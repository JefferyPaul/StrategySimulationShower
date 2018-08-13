import pandas as pd
import numpy as np
import os
from datetime import *
import matplotlib.pyplot as plt
import matplotlib.ticker


class ShowSignal(object):
	def __init__(self, ticker):
		self.ticker = ticker
		self.signal = pd.DataFrame()
		self.std_signal = pd.DataFrame()
		self.mkdata = pd.DataFrame()
		self.strategies = []
		self.period_fixed_std_signal = {}
		self.period_fixed_mkdata = {}

	# 收集信号、行情数据
	def get_signal_and_mkdata(self):
		# 查看循环 /Simulation 中所有策略文件夹
		path_sim = os.path.join(os.getcwd(), 'Simulation')
		is_ticker_in_strategy = 0
		for strategy in os.listdir(path_sim):
			path_strategy = os.path.join(path_sim, strategy)
			if os.path.isdir(path_strategy):
				path_strategy_dir = os.listdir(path_strategy)
			else:
				continue

			# 判断此策略(文件夹)中是否有 所选Ticker
			name_trader = ""
			for str_dir in path_strategy_dir:
				if self.ticker == str_dir.split("@")[0]:
					name_trader = str_dir
					is_ticker_in_strategy = 1
					print("find TICKER in %s" % strategy)
					break
			if name_trader == "":
				print("not find TICKER in %s" % strategy)

			# 若有此Ticker，则查看 整理 处理其数据
			else:
				path_trader_folder = os.path.join(path_strategy, name_trader)
				path_trader_rawsignal = os.path.join(path_trader_folder, 'RawSignals.csv')

				df = pd.read_csv(path_trader_rawsignal)
				# 整理时间DT
				df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
				df['TimeDelta'] = pd.to_timedelta((df['Time']))
				df['DateTime'] = df['Date'] + df['TimeDelta']

				# self.signal 记录该ticker不同strategy的TargetPositon
				df_signal = df[['DateTime', 'TargetPosition']]
				df_signal = df_signal.set_index('DateTime')
				df_signal.rename(columns={'TargetPosition': strategy}, inplace=True)
				self.signal = self.signal.join(df_signal, how='outer')

				# self.mkprice 记录该ticker的行情数据OHLCV
				df_data = df[['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']]
				df_data = df_data.set_index('DateTime')
				self.mkdata = self.mkdata.combine_first(df_data)

		self.signal = self.signal.dropna(how='all')
		self.mkdata = self.mkdata.dropna(how='all')
		self.signal = self.signal.fillna(method='ffill')
		self.signal = self.signal.fillna(0)

		if is_ticker_in_strategy:
			return 1
		else:
			return 'Not Find Ticker'

	# 整理为标准化的Signal_TargetPosition
	def set_std_signal(self):
		max_target = {}
		for strategy in self.strategies:
			max_target[strategy] = max(abs(self.signal[strategy].max()), abs(self.signal[strategy].min()))
			self.std_signal[strategy] = round(self.signal[strategy] / max_target[strategy] * 10, 0)

	# 按周期period 整理数据
	def data_period_fix(self, period, way):
		period_fixed_std_signal = pd.DataFrame()
		period_fixed_mkdata = pd.DataFrame()
		if period != "":
			if way == "1":
				period_fixed_std_signal = self.std_signal.resample(period, label='right').mean()
				period_fixed_mkdata = pd.concat([self.mkdata['Open'].resample(period).first(),
				                          self.mkdata['High'].resample(period).max(),
				                          self.mkdata['Low'].resample(period).min(),
				                          self.mkdata['Close'].resample(period).last(),
				                          self.mkdata['Volume'].resample(period).sum()], axis=1)
				period_fixed_std_signal = period_fixed_std_signal.dropna()
				period_fixed_mkdata = period_fixed_mkdata.dropna()

				l = [i for i in period_fixed_std_signal.index if i in period_fixed_mkdata.index]
				period_fixed_mkdata = period_fixed_mkdata.ix[l]
				period_fixed_std_signal = period_fixed_std_signal.ix[l]
			# 最后值
			elif way == '0':
				pass

			self.period_fixed_std_signal[period] = period_fixed_std_signal
			self.period_fixed_mkdata[period] = period_fixed_mkdata

	# 数据展示
	def show_signal(self):
		# 1-获取、设置周期
		def get_period():
			print('("0": 1 minute; '
			      '"1": 5 minutes; '
			      '"2": 30 minutes; '
			      '"3": 1 hour; '
			      '"4": 1 day; '
			      '"5": 1 week; '
			      '"q": Break )')
			select_period = input('Select Period:   or BREAK:     ')
			if select_period == 'q':
				return 'q'
			else:
				str_period = {"0": "1min",
				              "1": "5min",
				              "2": "30min",
				              "3": "1H",
				              "4": "1B",
				              "5": "W-MON"}[select_period]
				return str_period

		# 2-时间范围
		def get_data_start_end():
			select_range_start = input('Start Date (yyyyMMdd):   ')
			select_range_end = input('End Date(yyyyMMdd):   ')
			if select_range_start:
				select_range_start = datetime.strptime(select_range_start, "%Y%m%d")
			if select_range_end:
				select_range_end = datetime.strptime(select_range_end, "%Y%m%d")
			return select_range_start, select_range_end

		# 用于规整x轴时间区间    [ mkdata的时间区间 也使用 signal的时间区间，保证两者x轴一致 ]
		def format_date(x, pos=None):
			thisind = np.clip(int(x+0.5), 0, N-1)
			return self.period_fixed_std_signal[period][dt_start:dt_end].index[thisind].strftime('%Y-%m-%d %H:%M:%S')

		# 获取周期-处理数据
		period = get_period()
		# 若输入period 则show
		if period != 'q':
			way = '1'
			if period not in self.period_fixed_std_signal.keys():
				self.data_period_fix(period, way)

			# 获取起始时间
			while True:
				dt_signal_start = self.period_fixed_std_signal[period].index[0]
				dt_signal_end = self.period_fixed_std_signal[period].index[-1]
				print('[ %s  ---  %s ]' % (dt_signal_start, dt_signal_end))

				dt_start, dt_end = get_data_start_end()
				if dt_start == '' or dt_start < dt_signal_start:
					dt_start = dt_signal_start
				if dt_end == '' or dt_end > dt_signal_end:
					dt_end = dt_signal_end
				if dt_start < dt_signal_end and dt_end > dt_signal_start:
					break
				else:
					print('the Input Time Range is Wrong ')

			# !!! show !!!
			N = len(self.period_fixed_std_signal[period][dt_start:dt_end])
			ind = np.arange(N)

			fig = plt.figure()
			ax1 = fig.add_subplot(2, 1, 1)
			ax2 = ax1.twinx()
			ax3 = fig.add_subplot(2, 1, 2)
			if dt_start and dt_end:
				ax1.plot(ind, self.period_fixed_std_signal[period][dt_start:dt_end])
				ax2.plot(ind, self.period_fixed_mkdata[period][['Open', 'High', 'Low', 'Close']][dt_start:dt_end])
				ax3.plot(ind, self.period_fixed_mkdata[period]['Volume'][dt_start:dt_end])

				ax1.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_date))
				ax2.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_date))
				ax3.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(format_date))
				ax3.set_xlabel('DateTime')

				ax1.legend(self.period_fixed_std_signal[period].columns, loc='best')
				plt.show()

			return 1
		else:
			return 0

	# 保存数据与图片
	# def save_data(self):
	# 	std_signal_fixed.to_csv('%s@%s@%s-%s.csv' % (date.today(), self.ticker, 'signal', np.random.randint(1000)))
	# 	mkdata_fixed.to_csv('%s@%s@%s-%s.csv' % (date.today(), self.ticker, 'mkprice', np.random.randint(1000)))

	def run_main(self):
		if self.get_signal_and_mkdata() == 'Not Find Ticker':
			print('Not Find Ticker')
		else:
			self.strategies = self.signal.columns.values.tolist()
			self.set_std_signal()
			while True:
				is_continue_show_signal = self.show_signal()
				if not is_continue_show_signal:
					break
