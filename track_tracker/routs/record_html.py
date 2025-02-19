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
    # create_record_html_page,
    # filter_records_html_page,
    # find_record_html_page,
    # record_base_page,
    unimplemented_page,
    )

context = ContextSingleton()

router = APIRouter(
    prefix='/html/record',
    tags=['record', 'html'],
)
'''HTML pages for viewing and filtering different results for school or state records.'''


@router.get('/')
async def html_record(request: Request):
    record_page = unimplemented_page()
    return HTMLResponse(content=record_page, status_code=200)

# path = '/today'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_records_today(request: Request):
#     now = datetime.now()
#     morning = datetime(now.year, now.month, now.day)
#     evening = morning + timedelta(days=1)
#     record_page = filter_records_html_page(
#         datetime_start=morning,
#         datetime_end=evening
#     )
#     return HTMLResponse(content=record_page, status_code=200)

# path = '/this-month'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_records_today(request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, 1)
#     last_day = first_day.replace(month=first_day.month + 1)
#     record_page = filter_records_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=record_page, status_code=200)

# path = '/in-the-next-{number_of_days}-days'
# @router.get(path)
# @explicit_router.get(path)
# @clean_router.get(path)
# async def html_records_today(number_of_days: int, request: Request):
#     now = datetime.now()
#     first_day = datetime(now.year, now.month, now.day)
#     last_day = first_day + timedelta(days=number_of_days)
#     record_page = filter_records_html_page(
#         datetime_start=first_day,
#         datetime_end=last_day
#     )
#     return HTMLResponse(content=record_page, status_code=200)

# # @router.get('/modify')
# # async def html_modify_record(request: Request):
# #     record_page = create_record_html_page()
# #     return HTMLResponse(content=record_page, status_code=200)


# @router.get('/{record_uid}')
# async def html_record_record_uid(request: Request, record_uid: str):
#     eh = EventHandler()
#     try:
#         record = await eh.find_record(record_uid=record_uid)
#     # except MissingRecordException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     # except DuplicateRecordsException as err:
#     #     context.logger.error(f"ERROR: {err}")
#     #     raise HTTPException(status_code=404, detail=str(err))
#     except Exception as err:
#         context.logger.error(f'ERROR: {err}')
#         raise HTTPException(status_code=500, detail='Internal Server Error')
#     record_page = find_record_html_page(record=record)
#     return HTMLResponse(content=record_page, status_code=200)
