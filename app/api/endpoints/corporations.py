from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import corporation_crud
from app.core.db import get_session
from app.schemas.corporations import (
    CorporationList,
)


router = APIRouter(prefix="/corporations")


# по стэку в тз postgre не указан - подразумевается использование sqlite (?) (а значит без postGIS)
# так бы я реализовывал с помощью него скорей всего
# или с помощью чата запросил бы формулу Хаверсайна и встроил в круд
# но в рамках тестового и стэка - мне кажется приемлемым такой вариант
# (на случай больших радиусов можно просто запрашивать несколько раз, сдвигая точку c шагом 45км)
@router.get("")
async def list_corporations(
    name: Optional[str] = None,
    activity: Optional[str] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    perimeter: Optional[int] = Query(None, le=45),
    session: AsyncSession = Depends(get_session),
) -> list[CorporationList]:
    """Метод для поиска организаций по различным параметрам и вывода их списка."""
    return await corporation_crud.search(
        name, activity, longitude, latitude, perimeter, session
    )


@router.get("/{corporation_id}")
async def get_corporation(
    corporation_id: int, session: AsyncSession = Depends(get_session)
) -> CorporationList:
    """Метд для получения орг по id."""
    return await corporation_crud.get_by_id(corporation_id, session)
