from math import cos, radians

from sqlalchemy import Select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.buildings import Building
from app.models.activities import Activity
from app.models.corporations import Corporation


class CRUDCorporation(CRUDBase[Corporation]):
    def _base_query(self) -> Select[Corporation]:
        return (
            super()
            ._base_query()
            .options(
                selectinload(Corporation.phones),
                selectinload(Corporation.activities),
                selectinload(Corporation.building),
            )
        )

    async def filter_by_building(
        self, building_id: int, session: AsyncSession
    ) -> list[Corporation]:
        objs = await session.execute(
            self._base_query().where(Corporation.building_id == building_id)
        )
        return objs.scalars().all()

    async def filter_by_activity(
        self, activity_id: int, session: AsyncSession
    ) -> list[Corporation]:
        objs = await session.execute(
            self._base_query()
            .where(Corporation.activities.any(id=activity_id))
        )
        return objs.scalars().all()

    async def search(
        self,
        name: str | None,
        activity: str | None,
        lon: float | None,
        lat: float | None,
        perimeter: int | None,
        session: AsyncSession,
    ) -> list[Corporation]:
        filters = []
        if name:
            filters.append(Corporation.name.ilike(f"%{name}%"))
        if activity:
            filters.append(Corporation.activities.any(Activity.name.ilike(f"%{activity}%")))
        if lon and lat and perimeter:
            delta_lon = perimeter / 111
            delta_lat = perimeter / (111 * cos(radians(lat)))
            filters.append(
                Corporation.building.has(
                    and_(
                        Building.longitude.between(lon - delta_lon, lon + delta_lon),
                        Building.latitude.between(lat - delta_lat, lat + delta_lat),
                    )
                )
            )

        objs = await session.execute(self._base_query().where(and_(*filters)))
        return objs.scalars().all()
