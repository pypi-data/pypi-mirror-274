from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

from pymerc.api.models import common


class Building(BaseModel):
    """Represents a building."""

    capacity: Optional[int] = None
    construction: Optional[BuildingConstruction] = None
    delivery_cost: BuildingDeliveryCost
    id: int
    land: Optional[list[common.Location]] = None
    name: str
    owner_id: int
    producer: Optional[common.Producer] = None
    provider_id: Optional[int] = None
    size: Optional[int] = None
    storage: Optional[BuildingStorage] = None
    sublocation: Optional[common.Location] = None
    town_id: int
    type: common.BuildingType
    upgrades: Optional[list[common.BuildingUpgradeType]] = None


class BuildingConstruction(BaseModel):
    """Represents a construction on a building."""

    inventory: common.Inventory
    progress: int
    reference: str
    stage: str
    time: int
    upgrade_type: Optional[common.BuildingUpgradeType] = None


class BuildingDeliveryCost(BaseModel):
    """Represents the delivery cost of a building."""

    land_distance: float


class BuildingStorage(BaseModel):
    """Represents the storage of a building."""

    inventory: common.Inventory
    operations: list[str]
    reference: str
