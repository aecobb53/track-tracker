from calendar import month
from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import ContextSingleton
# from .html.unimplemented_page import unimplemented_page
from handlers import WorkoutHandler, AthleteHandler
from models import WorkoutFilter, AthleteFilter


from html import (
    # create_workout_html_page,
    # filter_workouts_html_page,
    # find_workout_html_page,
    # workout_base_page,
    # filter_workouts_html_page,
    filter_workouts_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/workout',
    tags=['workout', 'html'],
)


@router.get('/')
async def html_workout(request: Request):
    # mh = WorkoutHandler()
    # workouts = await mh.filter_workouts(workout_filter=WorkoutFilter())
    # ah = AthleteHandler()
    # for workout in workouts:
    #     athlete = await ah.find_athlete(AthleteFilter(uid=[workout.athlete_uid]))
    #     workout.athlete = athlete
    # workout_page = await filter_workouts_html_page(workouts=workouts)
    workout_page = await unimplemented_page()
    return HTMLResponse(content=workout_page, status_code=200)
