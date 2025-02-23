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
    prefix='/html/mark',
    tags=['mark', 'html'],
)


@router.get('/')
async def html_mark(request: Request):
    mark_page = await filter_marks_html_page()
    return HTMLResponse(content=mark_page, status_code=200)

# path = '/today'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_marks_today(request: Request):
#     now = datetime.now()
#     morning = datetime(now.year, now.month, now.day)
#     evening = morning + timedelta(days=1)
#     mark_page = filter_marks_html_page(
#         datetime_start=morning,
#         datetime_end=evening
#     )
#     return HTMLResponse(content=mark_page, status_code=200)

# path = '/this-month'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_marks_today(request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, 1)
#     last_day = first_day.replace(month=first_day.month + 1)
#     mark_page = filter_marks_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=mark_page, status_code=200)

# path = '/in-the-next-{number_of_days}-days'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_marks_today(number_of_days: int, request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, now.day)
#     last_day = first_day + timedelta(days=number_of_days)
#     mark_page = filter_marks_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=mark_page, status_code=200)

# # @router.get('/modify')
# # async def html_modify_mark(request: Request):
# #     mark_page = create_mark_html_page()
# #     return HTMLResponse(content=mark_page, status_code=200)


# @router.get('/{mark_uid}')
# async def html_mark_mark_uid(request: Request, mark_uid: str):
#     eh = EventHandler()
#     try:
#         mark = await eh.find_mark(mark_uid=mark_uid)
#     # except MissingRecordException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     # except DuplicateRecordsException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     except Exception as err:
#         context.logger.error(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Server Error')
#     mark_page = find_mark_html_page(mark=mark)
#     return HTMLResponse(content=mark_page, status_code=200)
