from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    """Базовая схема для дефтельностей организаций."""
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ActivityList(ActivityBase):
    """Схема для списка деятельностей."""
    pass

