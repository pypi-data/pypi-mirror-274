from pydantic import TypeAdapter

from pymerc.api.base import BaseAPI
from pymerc.api.models import buildings, common
from pymerc.util import data

BASE_URL = "https://play.mercatorio.io/api/buildings/"

class BuildingsAPI(BaseAPI):
    """A class for interacting with the buildings API endpoint."""

    async def get(self, id: int) -> buildings.Building:
        """Get a building by its ID.

        Args:
            id (int): The ID of the building.

        Returns:
            Building: The building.
        """
        response = await self.client.get(f"{BASE_URL}{id}")
        return buildings.Building.model_validate(response.json())

    async def set_manager(self, id: int, item: common.Item, manager: common.InventoryManager) -> bool:
        """Set the manager for an item in a building.

        Args:
            item (Item): The item.
            manager (InventoryManager): The manager.

        Returns:
            bool: Whether the manager was set.
        """
        json = data.convert_floats_to_strings(manager.model_dump(exclude_unset=True))
        response = await self.client.patch(f"{BASE_URL}{id}/storage/inventory/{item.name.lower()}", json=json)
        return response.status_code == 200
