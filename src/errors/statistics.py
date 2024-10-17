class ErrorAverageStatistics(Exception):
    def __init__(self, summa, amount):
        super().__init__()
        self.summa = summa
        self.amount = amount

    def __str__(self) -> str:
        return f'Average statistics error. Summa: {self.summa}. Amount: {self.amount}'