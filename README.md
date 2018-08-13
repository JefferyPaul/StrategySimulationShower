# StrategySimulationShower

TargetPositionShower.py： 控制任务流程。   
&emsp;方法：get_selected_data()： 一次性逐行读取，并通过Trader.add_raw_signals()读入以Trader类存放；   
&emsp;show_traders()：一次性输出图形。   
DataManger.py： 管理数据。方法：get_data_path()：返回所需数据的位置。   
Trader.py:	Trader类，记录trader信息如RawSignals、Pnls。    
&emsp;self.Rawsignals = {"DateTime":[], "TargetPosition":[], "MarketPrice":[], "Ticker":[]}   
&emsp;以字典-列表形式存储，方便直接合成DataFrame。  
&emsp;方法：add_raw_signals()  
Parese.py:方法： parse_raw_signaks_csv()： 识别RawSignals.csv数据，并以字典形式返回所需数据。  
