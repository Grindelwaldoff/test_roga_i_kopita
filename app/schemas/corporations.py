from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.buildings import BuildingList
from app.schemas.activities import ActivityList


class CorporationPhoneBase(BaseModel):
    """Базовая схма для телефонов организаций."""
    phone_number: str = Field(..., max_length=32)
    model_config = ConfigDict(from_attributes=True)


class CorporationPhoneList(CorporationPhoneBase):
    """Схема для списка телефонов организаций."""
    pass


class CorporationBase(BaseModel):
    """Базовая схема для организаций."""
    id: int
    name: str
    building: BuildingList
    phones: List[CorporationPhoneList]
    activities: List[ActivityList]
    model_config = ConfigDict(from_attributes=True)


class CorporationList(CorporationBase):
    """Схема для списка организаций."""
    pass
