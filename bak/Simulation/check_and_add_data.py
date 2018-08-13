import pandas as pd
import os
from datetime import *

def check_data_endtime():
	l_output = []
	path_cwd = os.getcwd()
	listdir_cwd = os.listdir(path_cwd)
	for name_strategy in listdir_cwd:
		print('Checking  %s' % name_strategy)
		path_strategy = os.path.join(path_cwd, name_strategy)
		if not(os.path.isdir(path_strategy)):
			continue
		listdir_strategy = os.listdir(path_strategy)
		for name_trader in listdir_strategy:
			path_trader = os.path.join(path_strategy, name_trader)
			if not(os.path.isdir(path_trader)):
				continue
			path_file_RawSignals = os.path.join(path_trader, 'RawSignals.csv')
			if not(os.path.isfile(path_file_RawSignals)):
				continue
			with open(path_file_RawSignals) as f_rawsiganls:
				df_rawsignals = pd.read_csv(f_rawsiganls)
				l_date = pd.to_datetime(df_rawsignals['Date'].iloc[-1], format='%Y-%m-%d')
				l_time = pd.to_timedelta(df_rawsignals['Time'].iloc[-1])
				end_datetime = l_date + l_time
			l = [name_strategy, name_trader, end_datetime]
			print(l)
			l_output.append(l)

	print(l_output)
	pd.DataFrame(l_output).to_csv('check_data_endtime.csv', header=None, index=False)

check_data_endtime()