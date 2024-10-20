import pytest

from errors.statistics import ErrorAverageStatistics
from schemas.coin_statistics import CoinStatistics
from schemas.transaction import TransactionOfStatistics, Direction
from services.statistic_calculator import StatisticFifoCalculator


class TestStatisticCalculator:
    def test_average_buy_empty(self):
        with pytest.raises(ValueError, match=r'.*[Tt]here are not buy.orders*'):
            StatisticFifoCalculator().calc_average_buy(buy_orders=[])

    def test_average_buy_error_average_all_negative(self):
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=1,
                amount_coin=2,
            ),
        ]
        with pytest.raises(ErrorAverageStatistics):
            StatisticFifoCalculator().calc_average_buy(buy_orders, initialize=(-100, -100))

    def test_average_buy_error_average_summa_non_positive(self):
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=1,
                amount_coin=2,
            ),
        ]
        with pytest.raises(ErrorAverageStatistics):
            StatisticFifoCalculator().calc_average_buy(buy_orders, initialize=(-1, -1))

    def test_average_buy_error_average_amount_non_positive(self):
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=1,
                amount_coin=2,
            ),
        ]
        with pytest.raises(ErrorAverageStatistics):
            StatisticFifoCalculator().calc_average_buy(buy_orders, initialize=(0, -10))

    def test_average_buy_default(self):
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=19.4,
                amount_coin=2000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=13.23,
                amount_coin=5000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=50,
                amount_coin=500000,
            ),
        ]
        actual_res = StatisticFifoCalculator().calc_average_buy(buy_orders=buy_orders)
        expected_res = CoinStatistics(
            symbol='',
            full_price=82.63,
            amount_coin=507000,
        )
        assert actual_res == expected_res

    def test_average_buy_set_index(self):
        index_start = 2
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=19.4,
                amount_coin=2000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=13.23,
                amount_coin=5000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=50,
                amount_coin=500000,
            ),
        ]
        actual_res = StatisticFifoCalculator().calc_average_buy(buy_orders=buy_orders, index_start=index_start)
        expected_res = CoinStatistics(
            symbol='',
            full_price=50,
            amount_coin=500000,
        )
        assert actual_res == expected_res

    def test_average_buy_set_initialize(self):
        index_start = 2
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=19.4,
                amount_coin=2000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=13.23,
                amount_coin=5000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=50,
                amount_coin=500000,
            ),
        ]
        actual_res = StatisticFifoCalculator().calc_average_buy(buy_orders=buy_orders, initialize=(10, 80))
        expected_res = CoinStatistics(
            symbol='',
            full_price=92.63,
            amount_coin=507080,
        )
        assert actual_res == expected_res

    def test_calc_empty(self):
        with pytest.raises(ValueError, match=r'.*[Tt]here are not buy.orders*'):
            StatisticFifoCalculator().calc([], [])

    def test_calc_empty_buy(self):
        buy_orders = []
        sell_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.SELL,
                amount_usdt=1,
                amount_coin=1,
            ),
        ]
        with pytest.raises(ValueError, match=r'.*[Tt]here are not buy.orders, but there are sell.orders*'):
            StatisticFifoCalculator().calc(buy_orders=buy_orders, sell_orders=sell_orders)

    def test_calc_empty_sell(self):
        sell_orders = []
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=19.4,
                amount_coin=2000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=13.23,
                amount_coin=5000,
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=50,
                amount_coin=500000,
            ),
        ]
        actual_res = StatisticFifoCalculator().calc(buy_orders=buy_orders, sell_orders=sell_orders)
        expected_res = CoinStatistics(
            symbol='',
            full_price=82.63,
            amount_coin=507000,
        )
        assert actual_res == expected_res

    def test_calc(self):
        buy_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=19.4,
                amount_coin=2000,
                # price = 0.0097
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=13.23,
                amount_coin=5000,
                # price = 0.002646
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.BUY,
                amount_usdt=50,
                amount_coin=500000,
                # price = 0.0001
            ),
        ]
        sell_orders: list[TransactionOfStatistics] = [
            TransactionOfStatistics(
                symbol='',
                direction=Direction.SELL,
                amount_usdt=40,
                amount_coin=1000,
                # price = 0.04
            ),
            TransactionOfStatistics(
                symbol='',
                direction=Direction.SELL,
                amount_usdt=1001,
                amount_coin=35750,
                # price = 0.028
            ),
        ]
        actual_res = StatisticFifoCalculator().calc(buy_orders=buy_orders, sell_orders=sell_orders)
        expected_res = CoinStatistics(
            symbol='',
            full_price=47.025,
            amount_coin=470250,
        )

        assert actual_res == expected_res
