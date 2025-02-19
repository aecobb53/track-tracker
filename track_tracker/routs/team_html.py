from calendar import month
from datetime import date, datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, ORJSONResponse

# from models import Event, EventFilter
# from handlers import EventHandler
# from handlers import EventHandler, parse_query_params
# from utils import parse_query_params, parse_header, MissingRecordException, DuplicateRecordsException
from models import ContextSingleton


from html import (
    # create_team_html_page,
    # filter_teams_html_page,
    # find_team_html_page,
    # team_base_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/team',
    tags=['team', 'html'],
)
'''HTML pages for viewing and filtering different athletes or results based on team.'''


@router.get('/')
async def html_team(request: Request):
    team_page = unimplemented_page()
    return HTMLResponse(content=team_page, status_code=200)

# path = '/today'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_teams_today(request: Request):
#     now = datetime.now()
#     morning = datetime(now.year, now.month, now.day)
#     evening = morning + timedelta(days=1)
#     team_page = filter_teams_html_page(
#         datetime_start=morning,
#         datetime_end=evening
#     )
#     return HTMLResponse(content=team_page, status_code=200)

# path = '/this-month'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_teams_today(request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, 1)
#     last_day = first_day.replace(month=first_day.month + 1)
#     team_page = filter_teams_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=team_page, status_code=200)

# path = '/in-the-next-{number_of_days}-days'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_teams_today(number_of_days: int, request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, now.day)
#     last_day = first_day + timedelta(days=number_of_days)
#     team_page = filter_teams_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=team_page, status_code=200)

# # @router.get('/modify')
# # async def html_modify_team(request: Request):
# #     team_page = create_team_html_page()
# #     return HTMLResponse(content=team_page, status_code=200)


# @router.get('/{team_uid}')
# async def html_team_team_uid(request: Request, team_uid: str):
#     eh = EventHandler()
#     try:
#         team = await eh.find_team(team_uid=team_uid)
#     # except MissingRecordException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     # except DuplicateRecordsException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     except Exception as err:
#         context.logger.error(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Server Error')
#     team_page = find_team_html_page(team=team)
#     return HTMLResponse(content=team_page, status_code=200)
