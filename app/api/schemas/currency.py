from pydantic import BaseModel


class ExchangeCurrency(BaseModel):
    base_cur: str
    cur_to: str
    amount: float = 1


class HistoryExchangeCurrency(ExchangeCurrency):
    date: str

