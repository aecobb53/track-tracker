from .athlete_html import router as athlete_router
from .dev_html import router as dev_html_router
from .group_html import router as group_html_router
from .meetday_html import router as meetday_html_router
from .result_html import router as result_html_router
from .team_html import router as team_html_router
from .workout_html import router as workout_html_router

from fastapi import APIRouter

from models import ContextSingleton


context = ContextSingleton()

router = APIRouter(
    prefix='/html',
    tags=['html'],
)

router.include_router(athlete_router)
router.include_router(dev_html_router)
router.include_router(group_html_router)
router.include_router(meetday_html_router)
router.include_router(result_html_router)
router.include_router(team_html_router)
router.include_router(workout_html_router)
