from show_signal.showsignal import *

# 控制显示选择
while True:
	dict_signal = {}
	select_st = input('Start("") or Exit("0") :    ')
	select_ticker = ''
	if select_st == "0":
		break
	elif select_st == "":
		select_ticker = input('Select Ticker :   ')

	dict_signal[select_ticker] = ShowSignal(select_ticker)
	dict_signal[select_ticker].run_main()