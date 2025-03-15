from calendar import month
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


from html import (
    filter_teams_html_page,
    find_team_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/team',
    tags=['team'],
)
'''HTML pages for viewing and filtering different teams or results based on team.'''


@router.get('/')
async def html_teams(request: Request):
    team_page = await filter_teams_html_page()
    return HTMLResponse(content=team_page, status_code=200)


@router.get('/{team_name}')
async def html_team(team_name: str, request: Request):
    ah = AthleteHandler()
    athletes = await ah.filter_athletes(AthleteFilter(team=[team_name]))
    mh = ResultHandler()
    results = await mh.filter_results(ResultFilter(team=[team_name]))
    team_page = await find_team_html_page(athletes=athletes, results=results, team_name=team_name)
    return HTMLResponse(content=team_page, status_code=200)

@router.get('/{team_name}/{season_year}')
async def html_team(team_name: str, season_year: int, request: Request):
    ah = AthleteHandler()
    athletes = await ah.filter_athletes(AthleteFilter(team=[team_name]))
    mh = ResultHandler()
    result_filter = ResultFilter(team=[team_name], meet_date=[f"After{season_year}-01-01", f"Before{season_year}-12-31"])
    results = await mh.filter_results(result_filter)
    team_page = await find_team_html_page(athletes=athletes, results=results, team_name=team_name, season_year=season_year)
    return HTMLResponse(content=team_page, status_code=200)
