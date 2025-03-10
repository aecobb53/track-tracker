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
from handlers import ResultHandler, AthleteHandler
from models import ResultFilter, AthleteFilter


from html import (
    # create_workout_html_page,
    # filter_workouts_html_page,
    # find_workout_html_page,
    # workout_base_page,
    # filter_workouts_html_page,
    # filter_workouts_html_page,
    sprint_html_page,
    hurlde_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/groups',
    tags=['groups', 'html'],
)


@router.get('/sprint')
async def html_sprint(request: Request):
    # mh = WorkoutHandler()
    # workouts = await mh.filter_workouts(workout_filter=WorkoutFilter())
    rh = ResultHandler()
    ah = AthleteHandler()
    athlete_filter = AthleteFilter(tags=['Sprint'])
    athletes = await ah.filter_athletes(athlete_filter=athlete_filter)
    athletes_dict = {}
    for athlete in athletes:
        result_filter = ResultFilter(athlete_uid=[athlete.uid])
        results = await rh.filter_results(result_filter=result_filter)
        valid_athlete = False
        for result in results:
            if ' 100' in result.event:
                valid_athlete = True
                break
            if ' 200' in result.event:
                valid_athlete = True
                break
            if ' 400' in result.event:
                valid_athlete = True
                break
        if not valid_athlete:
            continue
        athletes_dict[athlete.uid] = {
            'athlete': athlete,
            'results': results}

    sprint_page = await sprint_html_page(athletes_dict=athletes_dict)
    return HTMLResponse(content=sprint_page, status_code=200)

@router.get('/hurdle')
async def html_sprint(request: Request):
    rh = ResultHandler()
    ah = AthleteHandler()
    athlete_filter = AthleteFilter(tags=['Sprint'])
    athletes = await ah.filter_athletes(athlete_filter=athlete_filter)
    athletes_dict = {}
    for athlete in athletes:
        if not athlete.athlete_metadata:
            continue
        result_filter = ResultFilter(athlete_uid=[athlete.uid])
        results = await rh.filter_results(result_filter=result_filter)
        # valid_athlete = False
        # for result in results:
        #     # print(f"RESULT: {result}")
        #     if 'Hurdle' in result.event:
        #         valid_athlete = True
        #         break
        # if not valid_athlete:
        #     continue
        athletes_dict[athlete.uid] = {
            'athlete': athlete,
            'results': results}
    hurdle_page = await hurlde_html_page(athletes_dict=athletes_dict)
    return HTMLResponse(content=hurdle_page, status_code=200)

@router.get('/field')
async def html_sprint(request: Request):
    # mh = WorkoutHandler()
    # workouts = await mh.filter_workouts(workout_filter=WorkoutFilter())
    # ah = AthleteHandler()
    # for workout in workouts:
    #     athlete = await ah.find_athlete(AthleteFilter(uid=[workout.athlete_uid]))
    #     workout.athlete = athlete
    # workout_page = await filter_workouts_html_page(workouts=workouts)
    workout_page = await unimplemented_page()
    return HTMLResponse(content=workout_page, status_code=200)

@router.get('/distance')
async def html_sprint(request: Request):
    # mh = WorkoutHandler()
    # workouts = await mh.filter_workouts(workout_filter=WorkoutFilter())
    # ah = AthleteHandler()
    # for workout in workouts:
    #     athlete = await ah.find_athlete(AthleteFilter(uid=[workout.athlete_uid]))
    #     workout.athlete = athlete
    # workout_page = await filter_workouts_html_page(workouts=workouts)
    workout_page = await unimplemented_page()
    return HTMLResponse(content=workout_page, status_code=200)
