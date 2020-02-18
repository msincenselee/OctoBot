#  Drakkar-Software OctoBot
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

from abc import ABCMeta, abstractmethod
from os import path

from octobot_backtesting.api.backtesting import stop_independent_backtesting
from octobot_backtesting.constants import CONFIG_BACKTESTING
from tentacles.Evaluator import Strategies
from octobot_evaluators.evaluator.strategy_evaluator import StrategyEvaluator
from octobot_commons.tentacles_management.class_inspector import get_class_from_string, evaluator_parent_inspection

from octobot_evaluators.constants import CONFIG_EVALUATOR

DEFAULT_SYMBOL = "ICX/BTC"
DATA_FILE_PATH = "tests/static/"


SYMBOLS = {
    "Bitcoin": {
      "pairs": ["BTC/USDT"]
    },
    "Neo": {
      "pairs": ["NEO/BTC"]
    },
    "Ethereum": {
      "pairs": ["ETH/USDT"]
    },
    "Icon": {
      "pairs": ["ICX/BTC"]
    },
    "VeChain": {
      "pairs": ["VEN/BTC"]
    },
    "Nano": {
      "pairs": ["XRB/BTC"]
    },
    "Cardano": {
      "pairs": ["ADA/BTC"]
    },
    "Ontology": {
      "pairs": ["ONT/BTC"]
    },
    "Stellar": {
      "pairs": ["XLM/BTC"]
    },
    "Power Ledger": {
      "pairs": ["POWR/BTC"]
    },
    "Ethereum Classic": {
      "pairs": ["ETC/BTC"]
    },
    "WAX": {
      "pairs": ["WAX/BTC"]
    },
    "XRP": {
      "pairs": ["XRP/BTC"]
    },
    "Verge": {
      "pairs": ["XVG/BTC"]
    }
}

DATA_FILES_FOLDER = path.join(CONFIG_BACKTESTING, path.join("strategy_optimizer", "data_files"))

DATA_FILES = {
    "ADA/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581774950.9324272.data"),
    "BTC/USDT": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581774962.1269426.data"),
    "ETH/USDT": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581776676.5721796.data"),
    "ICX/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581774974.669779.data"),
    "NEO/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581774982.726014.data"),
    "VEN/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581774995.2311237.data"),
    "XRB/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775026.9255266.data"),
    "ONT/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581774988.7215023.data"),
    "XLM/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775018.2658834.data"),
    "POWR/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581776404.9679003.data")
}

EXTENDED_DATA_FILES = {
    "ADA/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775117.1713624.data"),
    "ETC/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775133.1533682.data"),
    "NEO/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775139.0332782.data"),
    "WAX/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775144.480404.data"),
    "XRP/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775149.6372743.data"),
    "XVG/BTC": path.join(DATA_FILES_FOLDER, "AbstractExchangeHistoryCollector_1581775154.2598503.data")
}


class AbstractBacktestingTest:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.config = {}
        self.strategy_evaluator_class = None

    def initialize_with_strategy(self, strategy_evaluator_class, config):
        self.config = config
        self.strategy_evaluator_class = strategy_evaluator_class
        self._register_only_strategy(strategy_evaluator_class)

    # plays a backtesting market profitability:
    # 1. ICX/BTC[30m]: -13.704206241519667 % (binance_ICX_BTC_20180716_131148)
    @staticmethod
    @abstractmethod
    async def test_default_run(strategy_tester):
        raise NotImplementedError("test_default_run not implemented")

    # plays a backtesting on a slow downtrend market:
    # 1. ICX/BTC[30m]: -13.704206241519667 % (binance_ICX_BTC_20180716_131148)
    # 2. NEO/BTC[30m]: -41.09080962800873 % (bittrex_NEO_BTC_20180722_195942)
    # 3. ONT/BTC[30m]: -17.9185520361991 % (binance_ONT_BTC_20180722_230900)
    # 4. XVG/BTC[30m]: -47.29729729729728 % (bittrex_XVG_BTC_20180726_211225)
    @staticmethod
    @abstractmethod
    async def test_slow_downtrend(strategy_tester):
        raise NotImplementedError("test_slow_downtrend not implemented")

    # plays a backtesting on a sharp downtrend market:
    # 1. VEN/BTC[30m] -35.26645213762865 % (binance_VEN_BTC_20180716_131148)
    # 2. XRP/BTC[30m]: -47.41750358680059 (vs btc) % (bittrex_XRP_BTC_20180726_210927)
    @staticmethod
    @abstractmethod
    async def test_sharp_downtrend(strategy_tester):
        raise NotImplementedError("test_sharp_downtrend not implemented")

    # plays a backtesting flat markets profitability:
    # 1. NEO/BTC[30m] -11.80763473053894 % (binance_NEO_BTC_20180716_131148)
    # 2. XRB/BTC[30m] -3.5209457722950255 % (binance_XRB_BTC_20180716_131148)
    # 3. ADA/BTC[30m] -6.140724946695086 % (bittrex_ADA_BTC_20180722_223357)
    # 4. WAX/BTC[30m] -8.77598152424941 % (bittrex_WAX_BTC_20180726_205032)
    @staticmethod
    @abstractmethod
    async def test_flat_markets(strategy_tester):
        raise NotImplementedError("test_flat_markets not implemented")

    # plays a backtesting with this strategy on a slow uptrend market:
    # 1. BTC/USDT[30m]: 17.20394836443646 (vs btc) % (binance_BTC_USDT_20180428_121156)
    # 2. ADA/BTC[30m] 16.19613670133728 % (binance_ADA_BTC_20180722_223335)
    @staticmethod
    @abstractmethod
    async def test_slow_uptrend(strategy_tester):
        raise NotImplementedError("test_slow_uptrend not implemented")

    # plays a backtesting with this strategy on a slow uptrend market:
    # 1. XLM/BTC[30m]: 30.88185223016684 (vs btc) % (binance_XLM_BTC_20180722_234305)
    # 2. POWR/BTC[30m]: 12.28597871355852 (vs btc) % (binance_POWR_BTC_20180722_234855)
    @staticmethod
    @abstractmethod
    async def test_sharp_uptrend(strategy_tester):
        raise NotImplementedError("test_sharp_uptrend not implemented")

    # plays a backtesting with this strategy on a slow uptrend market followed by a slow downtrend market:
    # 1. ETC/BTC[30m] -6.428386403538222 % (bittrex_ETC_BTC_20180726_210341)
    @staticmethod
    @abstractmethod
    async def test_up_then_down(strategy_tester):
        raise NotImplementedError("test_up_then_down not implemented")

    @abstractmethod
    def _handle_results(self, independent_backtesting, profitability):
        raise NotImplementedError("_handle_results not implemented")

    @abstractmethod
    async def _run_backtesting_with_current_config(self, data_file_to_use):
        raise NotImplementedError("_run_backtesting_with_current_config not implemented")

    async def _run_and_handle_results(self, data_file, expected_profitability):
        independent_backtesting = await self._run_backtesting_with_current_config(data_file)
        self._handle_results(independent_backtesting, expected_profitability)
        await stop_independent_backtesting(independent_backtesting)

    async def run_test_default_run(self, profitability):
        await self._run_and_handle_results(DATA_FILES[DEFAULT_SYMBOL], profitability)

    async def run_test_slow_downtrend(self, profitability_1, profitability_2, profitability_3, profitability_4,
                                      skip_extended=False):
        # await self._run_and_handle_results(DATA_FILES["ICX/BTC"], profitability_1)
        # await self._run_and_handle_results(DATA_FILES["ONT/BTC"], profitability_2)
        if not skip_extended:
            await self._run_and_handle_results(EXTENDED_DATA_FILES["NEO/BTC"], profitability_3)
            await self._run_and_handle_results(EXTENDED_DATA_FILES["XVG/BTC"], profitability_4)

    async def run_test_sharp_downtrend(self, profitability_1, profitability_2, skip_extended=False):
        await self._run_and_handle_results(DATA_FILES["VEN/BTC"], profitability_1)
        if not skip_extended:
            await self._run_and_handle_results(EXTENDED_DATA_FILES["XRP/BTC"], profitability_2)

    async def run_test_flat_markets(self, profitability_1, profitability_2, profitability_3, profitability_4,
                                    skip_extended=False):
        await self._run_and_handle_results(DATA_FILES["NEO/BTC"], profitability_1)
        await self._run_and_handle_results(DATA_FILES["XRB/BTC"], profitability_2)
        if not skip_extended:
            await self._run_and_handle_results(EXTENDED_DATA_FILES["ADA/BTC"], profitability_3)
            await self._run_and_handle_results(EXTENDED_DATA_FILES["WAX/BTC"], profitability_4)

    async def run_test_slow_uptrend(self, profitability_1, profitability_2):
        await self._run_and_handle_results(DATA_FILES["BTC/USDT"], profitability_1)
        await self._run_and_handle_results(DATA_FILES["ADA/BTC"], profitability_2)

    async def run_test_sharp_uptrend(self, profitability_1, profitability_2):
        await self._run_and_handle_results(DATA_FILES["XLM/BTC"], profitability_1)
        await self._run_and_handle_results(DATA_FILES["POWR/BTC"], profitability_2)

    async def run_test_up_then_down(self, profitability_1, skip_extended=False):
        if not skip_extended:
            await self._run_and_handle_results(EXTENDED_DATA_FILES["ETC/BTC"], profitability_1)

    def _register_only_strategy(self, strategy_evaluator_class):
        for evaluator_name in self.config[CONFIG_EVALUATOR]:
            if get_class_from_string(evaluator_name, StrategyEvaluator, Strategies,
                                     evaluator_parent_inspection) is not None:
                self.config[CONFIG_EVALUATOR][evaluator_name] = False
        self.config[CONFIG_EVALUATOR][strategy_evaluator_class.get_name()] = True
