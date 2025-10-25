from fastapi import APIRouter

from app.api.endpoints.buildings import router as buildings_router
from app.api.endpoints.acitivities import router as activities_router
from app.api.endpoints.corporations import router as corporations_router

main_router = APIRouter(prefix='/api')
main_router.include_router(buildings_router, tags=['buildings'])
main_router.include_router(activities_router, tags=['activities'])
main_router.include_router(corporations_router, tags=['corporations'])

