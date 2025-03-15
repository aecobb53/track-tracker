from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import ContextSingleton
from handlers import AthleteHandler, ResultHandler
from models import AthleteFilter, ResultFilter
# from .html.unimplemented_page import unimplemented_page


from html import (
    filter_athletes_html_page,
    find_athletes_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/athlete',
    tags=['athlete'],
)
'''HTML pages for viewing and filtering different athletes.'''


@router.get('/')
async def html_athletes(request: Request):
    athlete_page = await filter_athletes_html_page()
    return HTMLResponse(content=athlete_page, status_code=200)


@router.get('/{athlete_uid}')
async def html_athlete(athlete_uid: str, request: Request):
    ah = AthleteHandler()
    athlete = await ah.find_athlete(AthleteFilter(uid=[athlete_uid]))
    mh = ResultHandler()
    results = await mh.filter_results(ResultFilter(athlete_uid=[athlete_uid]))
    athlete_page = await find_athletes_html_page(athlete=athlete, results=results)
    return HTMLResponse(content=athlete_page, status_code=200)

# path = '/today'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_athletes_today(request: Request):
#     now = datetime.now()
#     morning = datetime(now.year, now.month, now.day)
#     evening = morning + timedelta(days=1)
#     athlete_page = filter_athletes_html_page(
#         datetime_start=morning,
#         datetime_end=evening
#     )
#     return HTMLResponse(content=athlete_page, status_code=200)

# path = '/this-month'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_athletes_today(request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, 1)
#     last_day = first_day.replace(month=first_day.month + 1)
#     athlete_page = filter_athletes_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=athlete_page, status_code=200)

# path = '/in-the-next-{number_of_days}-days'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_athletes_today(number_of_days: int, request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, now.day)
#     last_day = first_day + timedelta(days=number_of_days)
#     athlete_page = filter_athletes_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=athlete_page, status_code=200)

# # @router.get('/modify')
# # async def html_modify_athlete(request: Request):
# #     athlete_page = create_athlete_html_page()
# #     return HTMLResponse(content=athlete_page, status_code=200)


# @router.get('/{athlete_uid}')
# async def html_athlete_athlete_uid(request: Request, athlete_uid: str):
#     eh = EventHandler()
#     try:
#         athlete = await eh.find_athlete(athlete_uid=athlete_uid)
#     # except MissingRecordException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     # except DuplicateRecordsException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     except Exception as err:
#         context.logger.error(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Server Error')
#     athlete_page = find_athlete_html_page(athlete=athlete)
#     return HTMLResponse(content=athlete_page, status_code=200)
