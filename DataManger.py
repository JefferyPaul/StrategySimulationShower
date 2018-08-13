import os
from datetime import *


def get_config():
	return r"F:\StrategySimulationShower\Simulation"


def get_data_path(chose_strategies, chose_traders):
	path_root = r'F:\SimulationData\SimulationLog'
	dict_data_folder_path = {}
	for strategy_name in os.listdir(path_root):
		if type(chose_strategies) == list and strategy_name not in chose_strategies:
			continue
		path_strategy = os.path.join(path_root, strategy_name)
		dict_data_folder_path[strategy_name] = {trader_name.split("@")[0]: os.path.join(path_strategy, trader_name)
		                                        for trader_name in os.listdir(path_strategy)
		                                        if trader_name.split("@")[0] in chose_traders}
	return dict_data_folder_path


def show_all_selectable_strategies_traders(self):
	pass