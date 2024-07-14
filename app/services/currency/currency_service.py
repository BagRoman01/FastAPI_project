from app.api.schemas.currency import ExchangeCurrency, HistoryExchangeCurrency
from app.utils.currency_API import fetch_data


class CurrencyService:
    BASE_URL = 'https://api.freecurrencyapi.com/v1'
    CURRENCIES_URL = f'{BASE_URL}/currencies'
    EXCHANGE_URL = f'{BASE_URL}/latest'
    HISTORICAL_EXCHANGE_URL = f'{BASE_URL}/historical'

    async def get_currencies(self, currencies: str = None):
        if currencies:
            params = {'currencies': currencies}
            return await fetch_data(url=self.CURRENCIES_URL, params=params)
        return await fetch_data(url=self.CURRENCIES_URL)

    async def exchange_currency(self, exchange: ExchangeCurrency):
        params = {'base_currency': exchange.base_cur, 'currencies': exchange.cur_to}
        data = await fetch_data(url=self.EXCHANGE_URL, params=params)
        return {key: value * exchange.amount for key, value in data['data'].items()}

    async def history_exchange_currency(self, exchange: HistoryExchangeCurrency):
        params = {'base_currency': exchange.base_cur,
                  'currencies': exchange.cur_to,
                  'date': exchange.date}
        data = await fetch_data(url=self.HISTORICAL_EXCHANGE_URL, params=params)
        for date, currencies in data['data'].items():
            data['data'][date] = {cur: value * exchange.amount for cur, value in currencies.items()}
        return data
