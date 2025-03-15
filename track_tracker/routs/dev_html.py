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
    project_dev_home_page,
    unimplemented_dev_page,
    tech_stack_html_page,
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/dev',
    tags=['dev'],
)
'''HTML pages for developer involvement.'''


@router.get('/', status_code=200)
@router.get('/home', status_code=200)
async def html_athletes(request: Request):
    developer_page = await project_dev_home_page()
    return HTMLResponse(content=developer_page, status_code=200)


@router.get('/tech-stack')
async def html_athlete(request: Request):
    recruiter_page = await tech_stack_html_page()
    return HTMLResponse(content=recruiter_page, status_code=200)


@router.get('/roadmap')
async def html_athlete(request: Request):
    recruiter_page = await unimplemented_dev_page()
    return HTMLResponse(content=recruiter_page, status_code=200)


@router.get('/service-info', status_code=200)
async def service_info(request: Request):
    service_info_page = await unimplemented_dev_page()
    return HTMLResponse(content=service_info_page)

# @router.get('/tech-stack')
# async def html_athlete(request: Request):
#     recruiter_page = await unimplemented_page()
#     return HTMLResponse(content=recruiter_page, status_code=200)



