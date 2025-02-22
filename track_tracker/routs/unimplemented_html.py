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


from html import (
    # create_mark_html_page,
    # filter_marks_html_page,
    # find_mark_html_page,
    # mark_base_page,
    filter_marks_html_page,
    unimplemented_page
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html',
    tags=['unimplemented'],
)


# @router.get('/mark')
# async def html_mark():
#     return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/athlete')
async def html_athlete():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/teams')
async def html_teams():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/records')
async def html_records():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/schedule')
async def html_schedule():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/resources')
async def html_resources():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/video')
async def html_video():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/request-data')
async def html_request_data():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/about')
async def html_about():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/roadmap')
async def html_roadmap():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/healthcheck')
async def html_healthcheck():
    return HTMLResponse(content=unimplemented_page(), status_code=200)

@router.get('/contact-me')
async def html_contact_me():
    return HTMLResponse(content=unimplemented_page(), status_code=200)
