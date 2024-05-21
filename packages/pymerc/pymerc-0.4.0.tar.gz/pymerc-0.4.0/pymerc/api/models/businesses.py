from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

from pymerc.api.models import common


class Business(BaseModel):
    """A business in the game."""

    account: BusinessAccount
    account_id: int
    building_ids: list[int]
    buildings: list[Building]
    contract_ids: list[str]
    id: int
    name: str
    owner_id: int
    transport_ids: list[int]


class BusinessAccount(BaseModel):
    """The account of a business."""

    id: int
    name: str
    owner_id: int
    assets: dict[common.Asset, BusinessAccountAsset]


class BusinessAccountAsset(BaseModel):
    """An asset in a business account."""

    balance: float
    reserved: float
    unit_cost: Optional[float] = None


class Building(BaseModel):
    """A building belonging to a business."""

    id: int
    type: common.BuildingType
