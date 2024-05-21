from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

from pymerc.api.models import common


class Player(BaseModel):
    username: str
    household: Household
    discord_id: str
    settings: Settings
    active: bool


class Household(BaseModel):
    id: str
    name: str
    town_id: int
    portrait: str
    gender: str
    account_id: str
    business_ids: list[str]
    prestige: float
    prestige_impacts: list[PrestigeImpact]
    workers: list[Worker]
    operations: list[str]
    caps: dict[str, int]
    sustenance: Sustenance


class PrestigeImpact(BaseModel):
    factor: str
    impact: float


class Worker(BaseModel):
    assignment: str
    capacity: int
    name: str
    skills: dict[common.Skill, float]


class Sustenance(BaseModel):
    reference: str
    inventory: common.Inventory
    provider_id: str


class Settings(BaseModel):
    sound_volume: int
    notifications: NotificationSettings
    commoners_splash: bool
    construction_splash: bool
    land_purchase_splash: bool
    operations_splash: bool
    production_splash: bool
    recipes_splash: bool
    sustenance_splash: bool
    trading_splash: bool
    trade_config_splash: bool
    welcome_splash: bool
    first_building_splash: bool
    warehouse_splash: bool


class NotificationSettings(BaseModel):
    discord: bool
    mutes: Optional[list[str]] = []
