from datetime import *
import pandas as pd
import numpy as np


def parse_raw_signals_csv(line_data):
	# line_data 为 f.readline()
	title = ["Date", "Time", "Trader", "Ticker",
	         "TargetPosition", "price", "ModifiedPosition",
	         "Open", "High", "Low", "Close", "Volume", "Bid", "Ask", "TradingSession", "InitX"]
	l_line_data = line_data.split(",")

	if len(title) != len(l_line_data):
		print("Wrong in parse_raw_signals \n %s" % line_data)
		dict_line_data = {}
		return dict_line_data

	n = 0
	dict_line_data = {}
	for i_title in title:
		n += 1
		dict_line_data[i_title] = l_line_data[n-1]
	dict_line_data['DateTime'] = datetime.strptime("%s-%s" % (dict_line_data["Date"], dict_line_data['Time']),
	                                               "%Y-%m-%d-%H:%M:%S")

	return {"DateTime": dict_line_data["DateTime"],
	        "TargetPosition": float(dict_line_data['TargetPosition']),
	        "MarketPrice": float(dict_line_data['Close']),
	        "Ticker": dict_line_data['Ticker'],
	        "Trader": dict_line_data['Trader']}


def parse_pnls():
	pass

