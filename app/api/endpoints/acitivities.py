from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import corporation_crud
from app.core.db import get_session
from app.schemas.corporations import CorporationList


router = APIRouter(prefix="/activities")


@router.get("/{activity_id}/corporations")
async def get_corporations_by_activity(
    activity_id: int, session: AsyncSession = Depends(get_session)
) -> list[CorporationList]:
    """Метод для вывода орг по деятельности."""
    return await corporation_crud.filter_by_activity(activity_id, session)
