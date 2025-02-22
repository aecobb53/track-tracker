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
    filter_teams_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/team',
    tags=['team', 'html'],
)
'''HTML pages for viewing and filtering different teams or results based on team.'''


@router.get('/')
async def html_team(request: Request):
    team_page = filter_teams_html_page()
    return HTMLResponse(content=team_page, status_code=200)


@router.get('/{team_uid}')
async def html_team(team_uid: str, request: Request):
    team_page = unimplemented_page()
    return HTMLResponse(content=team_page, status_code=200)
