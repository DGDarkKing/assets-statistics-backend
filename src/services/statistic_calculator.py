from copy import deepcopy

from errors.statistics import ErrorAverageStatistics
from schemas.coin_statistics import CoinStatistics
from schemas.transaction import Transaction, TransactionOfStatistics


class StatisticFifoCalculator:
    def calc(
            self,
            buy_orders: list[TransactionOfStatistics],
            sell_orders: list[TransactionOfStatistics],
    ) -> tuple[CoinStatistics, list[TransactionOfStatistics]]:
        if not sell_orders:
            return self.calc_average_buy(buy_orders), buy_orders
        elif not buy_orders:
            raise ValueError('There are not buy_orders, but there are sell_orders')

        buy_orders = deepcopy(buy_orders)
        buy_index, sell_index = 0, 0
        len_sell_orders = len(sell_orders)
        price, amount = buy_orders[buy_index].usdt_price, buy_orders[buy_index].amount_coin
        while sell_index < len_sell_orders:
            amount -= sell_orders[sell_index].amount_coin
            while amount < 0:
                buy_orders[buy_index].remaining_coin = 0
                buy_index += 1
                amount += buy_orders[buy_index].amount_coin
                if amount > 0:
                    buy_orders[buy_index].remaining_coin = amount
                    price = buy_orders[buy_index].usdt_price

            if amount == 0:
                buy_orders[buy_index].remaining_coin = 0
                buy_index += 1
                price, amount = buy_orders[buy_index].usdt_price, buy_orders[buy_index].amount_coin

            sell_index += 1
        buy_orders[buy_index].remaining_coin = amount

        return self.calc_average_buy(buy_orders, buy_index + 1, (price * amount, amount)), buy_orders

    def calc_average_buy(
            self,
            buy_orders: list[TransactionOfStatistics],
            index_start: int = 0,
            initialize: tuple[float, float] = None
    ) -> CoinStatistics:
        if not buy_orders:
            raise ValueError('There are not buy_orders')

        summa, amount = (0, 0) if not initialize else initialize
        for i in range(index_start, len(buy_orders)):
            summa += buy_orders[i].amount_usdt
            amount += buy_orders[i].amount_coin

        if ((summa > 0 and amount <= 0) or (summa <= 0 and amount > 0)
                or (summa < 0 and amount < 0)):
            raise ErrorAverageStatistics(summa, amount)

        return CoinStatistics(
            symbols=buy_orders[0].symbol,
            full_price=summa,
            amount_coin=amount
        )
