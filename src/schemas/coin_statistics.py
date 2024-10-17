from pydantic import BaseModel, Field, computed_field


class CoinStatistics(BaseModel):
    symbol: str | None = None
    full_price: float = Field(ge=0)
    amount_coin: float = Field(ge=0)

    @computed_field
    @property
    def avg_price(self) -> float | None:
        if self.full_price == 0 and self.amount_coin == 0:
            return None
        return self.full_price / self.amount_coin


