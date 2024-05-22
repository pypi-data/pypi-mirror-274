from typing import Any

from .exceptions import ResponseDataError
from .client import Client

class Meta:
    def __init__(self, cmc_id: int):
        self.cmc_id = cmc_id

    async def update(self, client: Client):
        # 'async with' raises AttributeError: __aenter__
        r = await client.get(
            endpoint="/v2/cryptocurrency/info",
            params={'id': self.cmc_id},
            close=True
        )

        try:
            self.meta.update(client)
            self.data = r['data'][str(self.cmc_id)]
        except KeyError:
            raise ResponseDataError(status=r['status'])
        
    def __getattr__(self, __name: str) -> Any:
        return self.data[__name]

class Currency:
    def __init__(self, cmc_id: int):
        self.meta = Meta(cmc_id)
        self.cmc_id = cmc_id

    async def update(self, client: Client):
        # 'async with' raises AttributeError: __aenter__
        r = await client.get(
            endpoint="/v2/cryptocurrency/quotes/latest",
            params={'id': self.cmc_id}
        )

        try:
            self.meta.update(client)
            self.data = r['data'][str(self.cmc_id)]
        except KeyError:
            raise ResponseDataError(status=r['status'])

    def __getattr__(self, __name: str) -> Any:
        return self.data[__name]