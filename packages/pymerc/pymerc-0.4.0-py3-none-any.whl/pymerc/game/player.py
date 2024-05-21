from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pymerc.api.models.buildings import Building
from pymerc.api.models.common import Asset, BuildingType, InventoryAccountAsset, InventoryFlow, Item

if TYPE_CHECKING:
    from pymerc.client import Client


class Player:
    """A higher level representation of a player in the game."""

    def __init__(self, client: Client):
        self._client = client

    async def load(self):
        """Loads the data for the player."""
        self.data = await self._client.player_api.get()
        self.business = await self._client.businesses_api.get(self.data.household.business_ids[0])

        storehouses = [
            building.id
            for building in self.business.buildings
            if building.type == BuildingType.Storehouse
        ]

        if storehouses:
            self.storehouse = await self._client.building(storehouses[0])
        else:
            self.storehouse = None

    @property
    def buildings(self) -> list[Building]:
        """The buildings the player owns."""
        return self.business.buildings

    @property
    def money(self) -> float:
        """The amount of money the player has."""
        return self.business.account.assets.get(Asset.Money).balance

    def get_item(self, item: Item) -> Optional[InventoryAccountAsset]:
        """Get an item from the player's storehouse.

        Args:
            item (Item): The item to get.

        Returns:
            Optional[InventoryAccountAsset]: The item, if it exists.
        """
        return self.storehouse.storage.inventory.account.assets.get(item, None)

    def get_item_flow(self, item: Item) -> Optional[InventoryFlow]:
        """Get the flow of an item from the player's storehouse.

        Args:
            item (Item): The item to get.

        Returns:
            Optional[InventoryFlow]: The flow of the item, if it exists.
        """
        return self.storehouse.storage.inventory.previous_flows.get(item, None)