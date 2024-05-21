from __future__ import annotations
import asyncio

import httpx

from pymerc.api.buildings import BuildingsAPI
from pymerc.api.businesses import BusinessesAPI
from pymerc.api.map import MapAPI
from pymerc.api.player import PlayerAPI
from pymerc.api.static import StaticAPI
from pymerc.api.towns import TownsAPI
from pymerc.exceptions import TurnInProgressException
from pymerc.game.building import Building
from pymerc.game.player import Player
from pymerc.game.town import Town


class Client:
    """A simple API client for the Mercatorio API."""

    session: httpx.AsyncClient
    token: str
    user: str

    buildings_api: BuildingsAPI
    businesses_api: BusinessesAPI
    map_api: MapAPI
    player_api: PlayerAPI
    static_api: StaticAPI
    towns_api: TownsAPI

    def __init__(self, user: str, token: str):
        self.session = httpx.AsyncClient(http2=True)
        self.user = user
        self.token = token

        self.session.headers.setdefault("X-Merc-User", self.user)
        self.session.headers.setdefault("Authorization", f"Bearer {self.token}")

        self.buildings_api = BuildingsAPI(self)
        self.businesses_api = BusinessesAPI(self)
        self.map_api = MapAPI(self)
        self.player_api = PlayerAPI(self)
        self.static_api = StaticAPI(self)
        self.towns_api = TownsAPI(self)

    async def close(self):
        await self.session.aclose()

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make a GET request to the given URL.

        Args:
            url (str): The URL to make the request to.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.get(url, **kwargs)

    async def patch(self, url: str, json: any, **kwargs) -> httpx.Response:
        """Make a PATCH request to the given URL.

        Args:
            url (str): The URL to make the request to.
            json (any): The JSON data to send in the request.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.patch(url, json=json, **kwargs)

    async def post(self, url: str, json: any, **kwargs) -> httpx.Response:
        """Make a POST request to the given URL.

        Args:
            url (str): The URL to make the request to.
            json (any): The JSON data to send in the request.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.post(url, json=json, **kwargs)

    async def put(self, url: str, json: any, **kwargs) -> httpx.Response:
        """Make a PUT request to the given URL.

        Args:
            url (str): The URL to make the request to.
            json (any): The JSON data to send in the request.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        return await self.session.put(url, json=json, **kwargs)

    async def building(self, id: int) -> Building:
        """Get a building by its ID.

        Args:
            id (int): The ID of the building.

        Returns:
            Building: The building with the given ID.
        """
        b = Building(self, id)
        await b.load()

        return b

    async def player(self) -> Player:
        """Get the current player.

        Returns:
            Player: The player.
        """
        p = Player(self)
        await p.load()

        return p

    async def town(self, town_id: int) -> Town:
        """Get a town by its ID.

        Args:
            town_id (int): The ID of the town.

        Returns:
            Town: The town with the given ID.
        """
        t = Town(self, town_id)
        await t.load()

        return t

    async def towns(self, filter: list[str] = []) -> list[Town]:
        """Get all towns.

        Args:
            filter (list[str], optional): Filter towns by name. Defaults to [].

        Returns:
            list[Town]: All towns.
        """
        tasks = []
        for town in await self.towns_api.get_all():
            if filter and town.name not in filter:
                continue
            tasks.append(self.town(town.id))
        return await asyncio.gather(*tasks)

    async def turn(client: Client) -> int:
        """Get the current turn number.

        Args:
            client (Client): The Mercatorio API client.

        Returns:
            int: The current turn number.
        """
        response = await client.get("https://play.mercatorio.io/api/clock")

        if "preparing next game-turn, try again in a few seconds" in response.text:
            raise TurnInProgressException("A turn is in progress")

        return response.json()["turn"]
