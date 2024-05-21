from pydantic import TypeAdapter

from pymerc.api.base import BaseAPI
from pymerc.api.models import businesses

BASE_URL = "https://play.mercatorio.io/api/businesses/"


class BusinessesAPI(BaseAPI):
    """A class for interacting with the businesses API endpoint."""

    async def get(self, id: int) -> businesses.Business:
        """Get a business by its ID.

        Args:
            id (int): The ID of the business to get

        Returns:
            Business: The business with the given ID
        """
        response = await self.client.get(f"{BASE_URL}{id}")
        return businesses.Business.model_validate(response.json())
