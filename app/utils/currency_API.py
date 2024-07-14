import aiohttp
from app.core.config import settings
from app.exceptions.currencies_exceptions import FetchError
from starlette import status

m_headers = {'apikey': settings.CURRENCY_API_KEY}


async def fetch_data(url: str, params: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=m_headers, params=params) as response:
            if response.status != status.HTTP_200_OK:
                raise FetchError(status_code=response.status)
            data = await response.json()
            return data
