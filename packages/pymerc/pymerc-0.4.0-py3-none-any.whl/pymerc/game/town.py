from __future__ import annotations

import math
from typing import TYPE_CHECKING, Optional

from pymerc.api.models.map import Region
from pymerc.api.models import towns as models
from pymerc.api.models import common

if TYPE_CHECKING:
    from pymerc.client import Client


class Town:
    """A higher level representation of a town in the game."""

    def __init__(self, client: Client, id: int):
        self._client = client
        self.id = id

    async def load(self):
        """Loads the data for the town."""
        self._data = await self._client.towns_api.get_data(self.id)
        self._market = await self._client.towns_api.get_market_data(self.id)

    @property
    def data(self) -> models.TownData:
        """The data for the town."""
        return self._data

    @property
    def market(self) -> dict[str, models.TownMarketItem]:
        """The market data for the town."""
        return self._market.markets

    @property
    def structures(self) -> dict[str, models.TownDomainStructure]:
        """The structures in the town."""
        structures = {}
        for domain in self._data.domain.values():
            if domain.structure is not None:
                structures[domain.structure.type] = domain.structure

        return structures

    @property
    def total_satisfaction(self) -> int:
        """The percent satisfaction of the town across all categories."""
        demands = sum(
            [category.products for category in self._data.commoners.sustenance], []
        )
        desire_total = sum(demand.desire for demand in demands)
        result_total = sum(demand.result for demand in demands)

        return math.ceil((result_total / desire_total) * 100)

    @property
    def total_structures(self) -> int:
        """The total number of structures in the town."""
        return len(
            [
                domain
                for domain in self._data.domain.values()
                if domain.structure is not None
            ]
        )

    @property
    def total_taxes(self) -> int:
        """The total taxes collected by the town."""
        return sum(self._data.government.taxes_collected.__dict__.values())

    async def fetch_market_item(self, name: str) -> models.TownMarketItemDetails:
        """Fetches the details for a market item.

        Args:
            name (str): The name of the item

        Returns:
            TownMarketItemDetails: The details for the item
        """
        return await self._client.towns.get_market_item(self.id, name)

    async def fetch_region(self) -> Region:
        """Fetches the region of the town.

        Returns:
            Region: The region of the town.
        """
        return await self._client.regions.get(self._data.region)

    def get_item(self, name: str) -> Optional[models.TownMarketItem]:
        """Gets an item from the market.

        Args:
            name (str): The name of the item

        Returns:
            Optional[TownMarketItem]: The item, if found
        """
        return self._market.markets.get(name)

    def get_structures(
        self, type: common.BuildingType
    ) -> list[models.TownDomainStructure]:
        """Gets structures of a given type in the town.

        Args:
            type (BuildingType): The type of structure to find

        Returns:
            list[TownDomainStructure]: The structures with the given type
        """
        return [
            domain.structure
            for domain in self._data.domain.values()
            if domain.structure is not None and domain.structure.type == type
        ]
